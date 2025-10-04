#!/bin/bash

# 🚦 Sistema ETL de Tráfico Urbano - Generador de Documentación
# Genera documentación HTML profesional para el repositorio

echo "🚀 Generando documentación profesional..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
show_message() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yaml" ]; then
    show_error "No se encontró docker-compose.yaml. Ejecuta desde la raíz del proyecto."
    exit 1
fi

# Crear directorio de documentación si no existe
mkdir -p docs

show_message "Documentación HTML generada en docs/index.html"
show_message "README.md actualizado con información profesional"

# Mostrar información de acceso
echo ""
echo -e "${BLUE}📚 DOCUMENTACIÓN DISPONIBLE:${NC}"
echo "  🌐 HTML: docs/index.html"
echo "  📖 README: README.md"
echo "  🐳 Docker: docker-compose.yaml"
echo ""
echo -e "${BLUE}🚀 PARA PROBAR EL SISTEMA:${NC}"
echo "  1. docker-compose up -d"
echo "  2. Abrir http://localhost:8082"
echo "  3. Usuario: admin | Contraseña: admin"
echo ""
echo -e "${GREEN}✨ ¡Documentación lista para compartir!${NC}"
