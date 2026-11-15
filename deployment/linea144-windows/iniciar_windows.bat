@echo off
title API Linea 144 - Servidor Local
echo Iniciando API Linea 144 con seguridad api_keys.json y auditoria CSV...
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
