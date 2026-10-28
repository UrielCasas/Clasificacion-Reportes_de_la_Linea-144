# **Clasificación de Riesgo- Línea 144**
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
├── notebooks/
│   ├── EDA_Linea144.ipynb
│   └── Tratamiento_Linea144.ipynb
│
├── README.md               # Información sobre el repositorio
└── requirements.txt        # Requisitos (librerias)              ¡POR AGREGAR!
```

<!--## 🛫 **Deployment **

Enlace a la app desplegada en :  https://traductortph.streamlit.app/-->

## 🛠️ Herramientas

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/)
<!--
[![edge-tts](https://img.shields.io/badge/edge--tts-0078D4?style=flat&logo=microsoftedge&logoColor=white)](https://pypi.org/project/edge-tts/)
[![deep-translator](https://img.shields.io/badge/deep--translator-4285F4?style=flat&logo=googletranslate&logoColor=white)](https://deep-translator.readthedocs.io/en/latest/)
[![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-3776AB?style=flat\&logo=python\&logoColor=white)](https://pypi.org/project/SpeechRecognition/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat\&logo=googlegemini\&logoColor=white)](https://gemini.google.com/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![os](https://img.shields.io/badge/os-3776AB?style=flat\&logo=python\&logoColor=white)](https://docs.python.org/es/3/library/os.html)
[![asyncio](https://img.shields.io/badge/asyncio-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/library/asyncio.html)
[![uuid](https://img.shields.io/badge/uuid-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/es/3/library/uuid.html)
[![glob](https://img.shields.io/badge/glob-3776AB?style=flat&logo=python&logoColor=white)](https://docs.python.org/3/library/glob.html)
-->

## 👥 **Autores**
- Arnaldo Antonio Fustet
- Uriel Maximiano Casas

