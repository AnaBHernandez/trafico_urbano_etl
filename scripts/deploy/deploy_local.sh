#!/bin/bash
# Script de despliegue local para el proyecto ETL de tráfico urbano
# Equivalente a Terraform + Cloud Build en entorno local

set -e

echo "🚀 INICIANDO DESPLIEGUE LOCAL - PROYECTO ETL TRÁFICO URBANO"
echo "=========================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que Docker esté instalado
log "Verificando Docker..."
if ! command -v docker &> /dev/null; then
    error "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

success "Docker y Docker Compose están instalados"

# Crear directorios necesarios
log "Creando estructura de directorios..."
mkdir -p data/bronze/$(date +%Y/%m/%d)
mkdir -p data/silver
mkdir -p data/golden
mkdir -p logs
mkdir -p plugins

success "Estructura de directorios creada"

# Generar datos de tráfico si no existen
log "Verificando datos de tráfico..."
if [ ! -f "data/sensores_trafico.csv" ]; then
    log "Generando datos de tráfico..."
    python3 scripts/generar_datos_trafico.py
    success "Datos de tráfico generados"
else
    success "Datos de tráfico ya existen"
fi

# Configurar base de datos SQLite
log "Configurando base de datos SQLite..."
python3 scripts/config/setup_sqlite_connection.py
success "Base de datos SQLite configurada"

# Parar contenedores existentes si están corriendo
log "Parando contenedores existentes..."
docker-compose down 2>/dev/null || true

# Construir y levantar servicios
log "Construyendo y levantando servicios Docker..."
docker-compose up -d --build

# Esperar a que los servicios estén listos
log "Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
log "Verificando estado de los servicios..."
if docker-compose ps | grep -q "Up"; then
    success "Servicios Docker levantados correctamente"
else
    error "Error al levantar servicios Docker"
    docker-compose logs
    exit 1
fi

# Verificar que Airflow esté accesible
log "Verificando acceso a Airflow..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        success "Airflow está accesible en http://localhost:8080"
        break
    fi
    attempt=$((attempt + 1))
    log "Intento $attempt/$max_attempts - Esperando Airflow..."
    sleep 10
done

if [ $attempt -eq $max_attempts ]; then
    error "Airflow no está accesible después de $max_attempts intentos"
    docker-compose logs airflow-webserver
    exit 1
fi

# Verificar DAGs
log "Verificando DAGs disponibles..."
sleep 10
DAGS=$(docker-compose exec -T airflow-webserver airflow dags list 2>/dev/null | grep -c "trafico" || echo "0")

if [ "$DAGS" -gt 0 ]; then
    success "DAGs de tráfico detectados: $DAGS"
else
    warning "No se detectaron DAGs de tráfico. Verificando logs..."
    docker-compose logs airflow-scheduler
fi

# Mostrar información de acceso
echo ""
echo "🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE"
echo "===================================="
echo ""
echo "📊 INFORMACIÓN DE ACCESO:"
echo "  • Airflow UI: http://localhost:8080"
echo "  • Usuario: admin"
echo "  • Contraseña: admin"
echo ""
echo "📁 DATOS DEL PROYECTO:"
echo "  • Base de datos: data/trafico_urbano.db"
echo "  • Logs: logs/"
echo "  • DAGs: dags/trafico_urbano/"
echo ""
echo "🚀 COMANDOS ÚTILES:"
echo "  • Ver logs: docker-compose logs -f"
echo "  • Parar servicios: docker-compose down"
echo "  • Reiniciar: docker-compose restart"
echo "  • Ver estado: docker-compose ps"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "  1. Abrir http://localhost:8080 en tu navegador"
echo "  2. Buscar DAG 'trafico_diario_urbano'"
echo "  3. Hacer clic en 'Trigger DAG'"
echo "  4. Monitorear la ejecución"
echo ""

success "¡Proyecto ETL de tráfico urbano desplegado correctamente!"