#!/bin/bash
set -e

echo "===== Instalando dependencias ====="
pip install -r requirements.txt

echo "===== Recolectando archivos estáticos ====="
python manage.py collectstatic --no-input --clear

echo "===== Ejecutando migraciones ====="
python manage.py migrate --no-input

echo "===== Build completado ====="
