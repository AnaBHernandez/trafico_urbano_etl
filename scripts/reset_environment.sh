#!/bin/bash
# Script de Automatización Total (Emergency Reset v2)
# Ejecutar desde la raíz del proyecto

set -e

echo "🛑 --- FASE 1: Limpieza Profunda (Nuclear) ---"
# Forzamos borrado manual por si Terraform tiene el estado desincronizado
docker rm -f trafico_airflow_webserver trafico_airflow_scheduler trafico_postgres 2>/dev/null || true
docker volume rm trafico_postgres_data 2>/dev/null || true

cd infrastructure/terraform
terraform destroy -auto-approve || true

echo "🚀 --- FASE 2: Despliegue Limpio ---"
terraform apply -auto-approve

echo "⏳ --- FASE 3: Esperando a la Base de Datos (30s) ---"
# Aumentamos el tiempo para garantizar que Postgres esté listo para conexiones
sleep 30

echo "🛠️ --- FASE 4: Inicialización de Esquema (DB Migrate) ---"
docker run --rm \
    --network trafico_urbano_network \
    -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres/airflow \
    trafico_airflow_custom:latest \
    airflow db migrate

echo "👤 --- FASE 5: Creación de Usuario Admin ---"
docker run --rm \
    --network trafico_urbano_network \
    -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres/airflow \
    trafico_airflow_custom:latest \
    airflow users create \
    --username admin --password admin \
    --firstname Admin --lastname User --role Admin --email admin@example.com

echo "🔄 --- FASE 6: Reinicio de Servicios ---"
docker restart trafico_airflow_webserver trafico_airflow_scheduler

echo "✅ --- VERIFICACIÓN FINAL ---"
docker ps --filter "name=trafico_"

echo "🎉 ¡SISTEMA RESTAURADO! Accede a http://localhost:8080"