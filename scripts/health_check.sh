#!/bin/bash

# 🏥 Health Check del Sistema ETL de Tráfico Urbano
# Autor: Ana Belén Hernández
# Descripción: Script para verificar que todos los componentes funcionan correctamente

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Función para imprimir resultados
print_check() {
    local status=$1
    local message=$2
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS${NC} $message"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    elif [ "$status" = "FAIL" ]; then
        echo -e "${RED}❌ FAIL${NC} $message"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    else
        echo -e "${YELLOW}⚠️  WARN${NC} $message"
    fi
}

echo "🏥 HEALTH CHECK - SISTEMA ETL DE TRÁFICO URBANO"
echo "================================================"
echo ""

# 1. Verificar Docker
echo "🐳 Verificando Docker..."
if command -v docker &> /dev/null; then
    print_check "PASS" "Docker está instalado"
else
    print_check "FAIL" "Docker no está instalado"
fi

# 2. Verificar Docker Compose
echo "🐳 Verificando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    print_check "PASS" "Docker Compose está instalado"
else
    print_check "FAIL" "Docker Compose no está instalado"
fi

# 3. Verificar servicios Docker
echo "🐳 Verificando servicios Docker..."
if docker-compose ps | grep -q "Up"; then
    print_check "PASS" "Servicios Docker están ejecutándose"
else
    print_check "FAIL" "Servicios Docker no están ejecutándose"
fi

# 4. Verificar PostgreSQL
echo "🗄️ Verificando PostgreSQL..."
if docker-compose ps postgres | grep -q "healthy"; then
    print_check "PASS" "PostgreSQL está funcionando correctamente"
else
    print_check "FAIL" "PostgreSQL no está funcionando"
fi

# 5. Verificar Airflow Webserver
echo "🌐 Verificando Airflow Webserver..."
if curl -s http://localhost:8082/health > /dev/null 2>&1; then
    print_check "PASS" "Airflow Webserver está accesible en puerto 8082"
else
    print_check "FAIL" "Airflow Webserver no está accesible"
fi

# 6. Verificar Airflow Scheduler
echo "⚙️ Verificando Airflow Scheduler..."
if docker-compose ps airflow-scheduler | grep -q "Up"; then
    print_check "PASS" "Airflow Scheduler está funcionando"
else
    print_check "FAIL" "Airflow Scheduler no está funcionando"
fi

# 7. Verificar estructura de buckets
echo "📁 Verificando estructura de buckets..."
if [ -d "buckets/bronze-bucket/raw_data" ] && [ -d "buckets/silver-bucket/processed" ] && [ -d "buckets/golden-bucket/database" ]; then
    print_check "PASS" "Estructura de buckets está correcta"
else
    print_check "FAIL" "Estructura de buckets incompleta"
fi

# 8. Verificar datos de ejemplo
echo "📊 Verificando datos de ejemplo..."
if [ -f "buckets/bronze-bucket/raw_data/sensores_trafico.csv" ]; then
    print_check "PASS" "Datos de ejemplo encontrados"
else
    print_check "WARN" "No se encontraron datos de ejemplo"
fi

# 9. Verificar base de datos
echo "🗄️ Verificando base de datos..."
if [ -f "buckets/golden-bucket/database/trafico_urbano.db" ]; then
    print_check "PASS" "Base de datos SQLite encontrada"
else
    print_check "WARN" "Base de datos SQLite no encontrada"
fi

# 10. Verificar DAGs
echo "🔄 Verificando DAGs..."
if docker exec trafico_urbano_etl-airflow-scheduler-1 airflow dags list 2>/dev/null | grep -q "trafico_diario_urbano"; then
    print_check "PASS" "DAGs están cargados correctamente"
else
    print_check "FAIL" "DAGs no están cargados"
fi

# 11. Verificar permisos
echo "🔐 Verificando permisos..."
if [ -w "buckets/golden-bucket/database/trafico_urbano.db" ] 2>/dev/null; then
    print_check "PASS" "Permisos de base de datos correctos"
else
    print_check "WARN" "Permisos de base de datos pueden necesitar ajuste"
fi

# 12. Verificar puertos
echo "🔌 Verificando puertos..."
if netstat -tuln 2>/dev/null | grep -q ":8082"; then
    print_check "PASS" "Puerto 8082 está en uso (Airflow)"
else
    print_check "WARN" "Puerto 8082 no está en uso"
fi

# Resumen final
echo ""
echo "📊 RESUMEN DEL HEALTH CHECK"
echo "=========================="
echo "Total de verificaciones: $TOTAL_CHECKS"
echo -e "✅ Exitosas: ${GREEN}$PASSED_CHECKS${NC}"
echo -e "❌ Fallidas: ${RED}$FAILED_CHECKS${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!${NC}"
    echo "🌐 Accede a: http://localhost:8082"
    echo "👤 Usuario: admin / Contraseña: admin"
elif [ $FAILED_CHECKS -le 2 ]; then
    echo ""
    echo -e "${YELLOW}⚠️ Sistema mayormente funcional con algunas advertencias${NC}"
else
    echo ""
    echo -e "${RED}🚨 Sistema con problemas significativos${NC}"
    echo "💡 Ejecuta: ./scripts/start_system.sh para reiniciar"
fi

echo ""
echo "🔧 Comandos útiles:"
echo "  • Reiniciar: docker-compose restart"
echo "  • Ver logs: docker-compose logs -f"
echo "  • Parar: docker-compose down"
echo "  • Ejecutar DAG: docker exec trafico_urbano_etl-airflow-scheduler-1 airflow dags trigger trafico_diario_urbano"
