# API Línea 144 (Seguridad JSON + Auditoría CSV)

1. **Pydantic**: Esquemas actualizados sin advertencias de obsolescencia (`ConfigDict` y `examples`).
2. **Gestión de múltiples API Keys (`api_keys.json`)**: Permite activar/desactivar claves y asignar un nombre de cliente a cada una sin reiniciar el servidor.
3. **Auditoría de uso (`logs_uso.csv`)**: Registra automáticamente fecha/hora, cliente, endpoint, estado HTTP y resumen de predicción.

## Pasos previos antes de ejecutar
Copia tus archivos entrenados `riesgo.joblib` y `volumen.joblib` dentro de la carpeta `modelos/` del entorno que vayas a utilizar:
- `linea144-windows/modelos/`
- `linea144-docker/modelos/`
- `linea144-render/modelos/`

## Claves de prueba incluidas en `api_keys.json`
- `linea144-web-2026-xyz` (Cliente: Frontend Web - Activa)
- `linea144-analisis-987` (Cliente: Equipo Analisis - Activa)
- `linea144-test-000` (Cliente: Prueba Desactivada - Inactiva)
