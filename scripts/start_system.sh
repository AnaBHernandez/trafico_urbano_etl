#!/bin/bash

# 🚦 Sistema ETL de Tráfico Urbano - Script de Inicio
# Autor: Ana Belén Hernández
# Descripción: Script para iniciar el sistema completo de manera automática

set -e  # Salir si hay algún error

echo "🚦 INICIANDO SISTEMA ETL DE TRÁFICO URBANO"
echo "=========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar prerrequisitos
print_status "Verificando prerrequisitos..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

print_success "Prerrequisitos verificados"

# Crear directorios necesarios
print_status "Creando estructura de directorios..."

mkdir -p buckets/bronze-bucket/raw_data
mkdir -p buckets/silver-bucket/processed
mkdir -p buckets/golden-bucket/database
mkdir -p buckets/backup-bucket
mkdir -p logs/scheduler
mkdir -p logs/webserver
mkdir -p logs/worker

print_success "Estructura de directorios creada"

# Configurar permisos
print_status "Configurando permisos..."

chmod -R 777 buckets/
chmod -R 777 logs/

print_success "Permisos configurados"

# Parar servicios existentes si los hay
print_status "Parando servicios existentes..."
docker-compose down -v 2>/dev/null || true

# Limpiar contenedores huérfanos
print_status "Limpiando contenedores huérfanos..."
docker system prune -f

# Iniciar servicios
print_status "Iniciando servicios Docker..."
docker-compose up -d

# Esperar a que los servicios estén listos
print_status "Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
print_status "Verificando estado de los servicios..."

# Verificar PostgreSQL
if docker-compose ps postgres | grep -q "healthy"; then
    print_success "PostgreSQL está funcionando"
else
    print_warning "PostgreSQL puede estar iniciando..."
fi

# Verificar Airflow Webserver
if curl -s http://localhost:8082/health > /dev/null; then
    print_success "Airflow Webserver está funcionando"
else
    print_warning "Airflow Webserver puede estar iniciando..."
fi

# Verificar Airflow Scheduler
if docker-compose ps airflow-scheduler | grep -q "Up"; then
    print_success "Airflow Scheduler está funcionando"
else
    print_warning "Airflow Scheduler puede estar iniciando..."
fi

# Mostrar información de acceso
echo ""
echo "🎉 SISTEMA INICIADO EXITOSAMENTE"
echo "================================"
echo ""
echo "🌐 Airflow UI: http://localhost:8082"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: admin"
echo ""
echo "📊 Comandos útiles:"
echo "  • Ver estado: docker-compose ps"
echo "  • Ver logs: docker-compose logs -f"
echo "  • Parar sistema: docker-compose down"
echo ""
echo "🚀 Para ejecutar un DAG:"
echo "  docker exec trafico_urbano_etl-airflow-scheduler-1 airflow dags trigger trafico_diario_urbano"
echo ""

# Verificar si hay datos de ejemplo
if [ -f "buckets/bronze-bucket/raw_data/sensores_trafico.csv" ]; then
    print_success "Datos de ejemplo encontrados"
    echo "📊 Datos disponibles:"
    echo "  • Sensores de tráfico: $(wc -l < buckets/bronze-bucket/raw_data/sensores_trafico.csv) registros"
    echo "  • Semáforos: $(wc -l < buckets/bronze-bucket/raw_data/semaforos.csv) registros"
    echo "  • Cámaras: $(wc -l < buckets/bronze-bucket/raw_data/camaras_seguridad.csv) registros"
    echo "  • Incidentes: $(wc -l < buckets/bronze-bucket/raw_data/incidentes_trafico.csv) registros"
    echo "  • Vehículos: $(wc -l < buckets/bronze-bucket/raw_data/vehiculos.csv) registros"
else
    print_warning "No se encontraron datos de ejemplo"
    echo "💡 Puedes generar datos con: python3 scripts/generar_datos_simple.py"
fi

echo ""
print_success "¡Sistema ETL de Tráfico Urbano listo para usar!"
echo "🎬 Perfecto para demostraciones y portfolios profesionales"
