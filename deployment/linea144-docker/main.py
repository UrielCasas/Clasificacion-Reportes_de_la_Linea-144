import os
import csv
import json
import secrets
from pathlib import Path
from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
import joblib
import pandas as pd

# Resolución de rutas independiente del sistema operativo
BASE_DIR = Path(__file__).resolve().parent
RUTA_MODELO_RIESGO = BASE_DIR / "modelos" / "riesgo.joblib"
RUTA_MODELO_VOLUMEN = BASE_DIR / "modelos" / "volumen.joblib"
RUTA_API_KEYS = BASE_DIR / "api_keys.json"
RUTA_LOGS_CSV = BASE_DIR / "logs_uso.csv"

# --- AUDITORÍA DE USO EN CSV ---
def registrar_auditoria(cliente: str, endpoint: str, estado: str, detalle: str):
    archivo_nuevo = not RUTA_LOGS_CSV.exists()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(RUTA_LOGS_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if archivo_nuevo:
                writer.writerow(["fecha_hora", "cliente", "endpoint", "estado", "detalle"])
            writer.writerow([timestamp, cliente, endpoint, estado, detalle])
    except Exception as e:
        print(f"[ERROR AUDITORÍA] No se pudo escribir en {RUTA_LOGS_CSV}: {e}")


# --- SEGURIDAD CON api_keys.json ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def verificar_api_key(request: Request, api_key_recibida: str = Security(api_key_header)) -> str:
    endpoint_actual = request.url.path

    if not api_key_recibida:
        registrar_auditoria("Anonimo", endpoint_actual, "401_RECHAZADO", "Falta cabecera X-API-Key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la cabecera 'X-API-Key'."
        )

    if not RUTA_API_KEYS.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Archivo api_keys.json no encontrado en el servidor."
        )

    try:
        with open(RUTA_API_KEYS, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al leer el formato de api_keys.json."
        )

    for registro in data.get("claves", []):
        if registro.get("activa", False):
            clave_valida = registro.get("key", "")
            if clave_valida and secrets.compare_digest(api_key_recibida, clave_valida):
                return registro.get("cliente", "Desconocido")

    registrar_auditoria("Clave_Invalida", endpoint_actual, "401_RECHAZADO", "API Key inválida o desactivada")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API Key inválida o desactivada."
    )


app = FastAPI(
    title="API Línea 144 - Riesgo y Demanda",
    description="API multiplataforma con autenticación JSON y auditoría de uso.",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelos en memoria al iniciar
try:
    modelo_riesgo = joblib.load(RUTA_MODELO_RIESGO)
    modelo_volumen = joblib.load(RUTA_MODELO_VOLUMEN)
except Exception as e:
    raise RuntimeError(f"Error al cargar los modelos en {BASE_DIR / 'modelos'}: {e}")


# Esquemas Pydantic V2
class EntradaRiesgo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edad_persona_en_situacion_de_violencia: float = Field(..., examples=[32.0])
    log_pobl_prov: float = Field(..., examples=[15.2])
    is_weekend: int = Field(..., ge=0, le=1, examples=[0])
    tipo_de_violencia_psicologica_si: int = Field(..., ge=0, le=1, examples=[1])
    tipo_de_violencia_simbolica_si: int = Field(..., ge=0, le=1, examples=[0])
    tipo_de_violencia_economica_y_patrimonial_si: int = Field(..., ge=0, le=1, examples=[1])
    tipo_de_violencia_domestica_si: int = Field(..., ge=0, le=1, examples=[1])
    modalidad_de_violencia_institucional_si: int = Field(..., ge=0, le=1, examples=[0])
    modalidad_de_violencia_laboral_si: int = Field(..., ge=0, le=1, examples=[0])
    modalidad_de_violencia_otras_si: int = Field(..., ge=0, le=1, examples=[0])
    vinculo_con_la_persona_agresora_pareja: int = Field(..., ge=0, le=1, examples=[1])
    vinculo_con_la_persona_agresora_ex_pareja: int = Field(
        ..., alias="vinculo_con_la_persona_agresora_ex pareja", ge=0, le=1, examples=[0]
    )
    vinculo_con_la_persona_agresora_otro: int = Field(..., ge=0, le=1, examples=[0])
    vinculo_con_la_persona_agresora_otro_familiar: int = Field(
        ..., alias="vinculo_con_la_persona_agresora_otro familiar", ge=0, le=1, examples=[0]
    )
    genero_persona_en_situacion_de_violencia_mujer: int = Field(..., ge=0, le=1, examples=[1])
    genero_persona_en_situacion_de_violencia_varon: int = Field(..., ge=0, le=1, examples=[0])
    genero_de_la_persona_agresora_varon: int = Field(..., ge=0, le=1, examples=[1])
    genero_de_la_persona_agresora_mujer: int = Field(..., ge=0, le=1, examples=[0])


class EntradaVolumen(BaseModel):
    fecha: date = Field(..., examples=["2026-11-16"])
    lag_1: float = Field(..., examples=[54.0])
    lag_7: float = Field(..., examples=[61.0])


@app.get("/")
def health_check():
    return {
        "estado": "activo",
        "version": "1.2.0",
        "seguridad": "api_keys.json activo",
        "auditoria": "logs_uso.csv activo",
        "modelos": ["riesgo.joblib", "volumen.joblib"]
    }


@app.post("/predecir/riesgo")
def predecir_riesgo(datos: EntradaRiesgo, cliente: str = Security(verificar_api_key)):
    try:
        fila = datos.model_dump(by_alias=True)
        columnas_ordenadas = [
            'edad_persona_en_situacion_de_violencia', 'log_pobl_prov', 'is_weekend',
            'tipo_de_violencia_psicologica_si', 'tipo_de_violencia_simbolica_si',
            'tipo_de_violencia_economica_y_patrimonial_si', 'tipo_de_violencia_domestica_si',
            'modalidad_de_violencia_institucional_si', 'modalidad_de_violencia_laboral_si',
            'modalidad_de_violencia_otras_si', 'vinculo_con_la_persona_agresora_pareja',
            'vinculo_con_la_persona_agresora_ex pareja', 'vinculo_con_la_persona_agresora_otro',
            'vinculo_con_la_persona_agresora_otro familiar',
            'genero_persona_en_situacion_de_violencia_mujer',
            'genero_persona_en_situacion_de_violencia_varon',
            'genero_de_la_persona_agresora_varon', 'genero_de_la_persona_agresora_mujer'
        ]
        
        df_input = pd.DataFrame([fila])[columnas_ordenadas]
        prediccion = int(modelo_riesgo.predict(df_input)[0])
        probabilidades = modelo_riesgo.predict_proba(df_input).tolist()[0]
        etiquetas = {1: "Medio", 2: "Alto"}
        etiqueta_res = etiquetas.get(prediccion, "Desconocido")

        registrar_auditoria(cliente, "/predecir/riesgo", "200_OK", f"Riesgo={etiqueta_res}")
        
        return {
            "nivel_riesgo_codigo": prediccion,
            "nivel_riesgo_etiqueta": etiqueta_res,
            "probabilidades": {
                "Medio": round(float(probabilidades[0]), 4),
                "Alto": round(float(probabilidades[1]), 4)
            }
        }
    except Exception as e:
        registrar_auditoria(cliente, "/predecir/riesgo", "500_ERROR", str(e))
        raise HTTPException(status_code=500, detail=f"Error en predicción de riesgo: {str(e)}")


@app.post("/predecir/volumen")
def predecir_volumen(datos: EntradaVolumen, cliente: str = Security(verificar_api_key)):
    try:
        features = {
            "dia_semana": datos.fecha.weekday(),
            "mes": datos.fecha.month,
            "dia": datos.fecha.day,
            "lag_1": datos.lag_1,
            "lag_7": datos.lag_7
        }
        columnas_ordenadas = ['dia_semana', 'mes', 'dia', 'lag_1', 'lag_7']
        df_input = pd.DataFrame([features])[columnas_ordenadas]
        prediccion = float(modelo_volumen.predict(df_input)[0])
        estimado_entero = round(prediccion)

        registrar_auditoria(
            cliente, "/predecir/volumen", "200_OK", f"Fecha={datos.fecha} | Estimado={estimado_entero}"
        )
        
        return {
            "fecha": str(datos.fecha),
            "llamadas_estimadas": round(prediccion, 2),
            "llamadas_estimadas_entero": estimado_entero
        }
    except Exception as e:
        registrar_auditoria(cliente, "/predecir/volumen", "500_ERROR", str(e))
        raise HTTPException(status_code=500, detail=f"Error en predicción de volumen: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
