# **Clasificación de Riesgo - Línea 144**
Trabajo final para la materia _Práctica Profesional: Análisis y Exploración de Datos_: Clasificador sobre situación de riesgo (alto o medio) de reportes de la línea 144 por tipología de violencia de género en las distintas provincias de Argentina que hubieron para proponer medidas exclusivas en los casos exuberantes.

Los resultados obtenidos sirven para los ministerios de desarrollo social, la Línea 144 y organizaciones de la sociedad civil con el fin de optimizar las líneas de atención.

<!-- Queremos clasificar si un reporte corresponde a una situación de alto o mediano riesgo, esto en base a la cantidad de reportes por tipología de violencia de género en las distintas provincias de Argentina que hubieron para proponer medidas exclusivas en los casos exuberantes. Los resultados obtenidos sirven para los ministerios de desarrollo social, la Línea 144 y organizaciones de la sociedad civil con el fin de optimizar las líneas de atención.
Los reportes se descargan en formato CSV desde la plataforma Kaggle (tiene un apróximado de 90 mil
registros desde el 2020 hasta el 2023) conteniendo históricos a nivel nacional: Línea 144 Argentina en Kaggle.
En el EDA analizaremos la información de cada reporte (fecha, provincia, genero de la victima como del
agresor, su vinculo y el/los tipos de violencia). Identificaremos con gráficos de barras las provincias con mayor volúmen de reportes y el tipo de agresión más recurrente, como también la correlación entre vinculo y tipo/s de agresión. Como modelo, se utilizara un algoritmo de clasificación para predecir la gravedad del caso. -->

<!-- La app solamente esta desplegado en _Streamlit_ para poder interactuar con el LLM basado en los motores de _Google Translator_ (de Google) y MyMemory (de Microsoft).-->

## 🏗️ **Estructura del Proyecto**
```text
.
│
├── data/                   # Evolución del dataset
│   ├── processed/
│   │    └── Dataset procesado de tipo .parquet
│   ├── raw/
│   │    └── Dataset crudo
│   └── raw_utf-8/
│        └── Dataset crudo codificado a utf-8
│
├── deployment/             # Despliegue de los modelos
│   ├── linea144-docker/
│   ├── linea144-frontend/
│   ├── linea144-render/
│   ├── linea144-windows/
│   ├── README.md
│   └── docker-compose.yml
│
├── modelos/                # Modelos entrenados
│   ├── riesgo.joblib
│   └── volumen.joblib
│
├── notebooks/              # Etapas sobre CRISP-DM
│   ├── training_captures/
│   │    └── Capturas de métricas obtenidas en la evaluación
│   ├── EDA_Linea144.ipynb
│   ├── Entrenamiento_Linea144.ipynb
│   ├── Entrenamiento_Linea144.py
│   └── Tratamiento_Linea144.ipynb
│
├── LICENSE                 # Licencia MIT
└── README.md               # Información sobre el repositorio
```

<!--## 🛫 **Deployment **

Enlace a la app desplegada en :  https://traductortph.streamlit.app/-->

## 🛠️ Herramientas

[![Jupyter Notebook](https://img.shields.io/badge/Jupyter%20Notebook-F37626?style=flat&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/)
[![Render](https://img.shields.io/badge/Render-000000?style=flat\&logo=render\&logoColor=white)](https://render.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat\&logo=html5\&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat\&logo=googlegemini\&logoColor=white)](https://gemini.google.com/)

<!--
[![edge-tts](https://img.shields.io/badge/edge--tts-0078D4?style=flat&logo=microsoftedge&logoColor=white)](https://pypi.org/project/edge-tts/)
[![deep-translator](https://img.shields.io/badge/deep--translator-4285F4?style=flat&logo=googletranslate&logoColor=white)](https://deep-translator.readthedocs.io/en/latest/)
[![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-3776AB?style=flat\&logo=python\&logoColor=white)](https://pypi.org/project/SpeechRecognition/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat\&logo=googlegemini\&logoColor=white)](https://gemini.google.com/)
[![Dockerfile](https://img.shields.io/badge/Dockerfile-2496ED?style=flat&logo=docker&logoColor=white)](https://docs.docker.com/reference/dockerfile/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![os](https://img.shields.io/badge/os-3776AB?style=flat\&logo=python\&logoColor=white)](https://docs.python.org/es/3/library/os.html)
[![asyncio](https://img.shields.io/badge/asyncio-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/library/asyncio.html)
[![uuid](https://img.shields.io/badge/uuid-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/library/uuid.html)
[![glob](https://img.shields.io/badge/glob-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/3/library/glob.html)
-->

## Probar en Windows
1. Colocá tus modelos `riesgo.joblib` y `volumen.joblib` dentro de la carpeta `modelos/`.
2. Instalá dependencias: `pip install -r requirements.txt`
3. Iniciá el servidor: `uvicorn main:app --reload`
4. En el navegador: http://127.0.0.1:8000/

## Despliegue en Render + Neon (PostgreSQL gratuito persistente)
1. Subí este proyecto a tu repositorio en GitHub (recordá colocar tus archivos `riesgo.joblib` y `volumen.joblib` dentro de la carpeta `modelos/`).
2. Creá una base gratuita en Neon y copiá la **Connection String** (`postgresql://...`).
3. En **Render**, entrá a tu servicio -> **Environment** y creá la variable:
   - **Key:** `DATABASE_URL`
   - **Value:** tu URL de conexión de Neon.
4. Si no configurás `DATABASE_URL` (por ejemplo al probar en tu PC local), la aplicación usará automáticamente una base SQLite en `datos/linea144.db`.

## Usuarios iniciales creados automáticamente
- **Superusuario (ve todo + gestión de usuarios):** `su` / clave: `su123`
- **Operador Riesgo (solo formulario 1):** `operador_riesgo` / clave: `123`
- **Planificador Volumen (solo formulario 2):** `planificador` / clave: `456`

## 👥 **Autores**
- Arnaldo Antonio Fustet
- Uriel Maximiano Casas

