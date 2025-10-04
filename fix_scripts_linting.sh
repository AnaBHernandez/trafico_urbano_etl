#!/bin/bash

echo "🔧 Corrigiendo errores de linting en scripts..."

# Función para limpiar espacios en blanco
clean_whitespace() {
    local file="$1"
    echo "  📝 Limpiando $file"
    
    # Eliminar espacios al final de líneas
    sed -i 's/[[:space:]]*$//' "$file"
    
    # Eliminar líneas vacías con espacios
    sed -i '/^[[:space:]]*$/d' "$file"
    
    # Asegurar que el archivo termine con salto de línea
    if [ -n "$(tail -c1 "$file")" ]; then
        echo "" >> "$file"
    fi
}

# Función para dividir líneas largas
fix_long_lines() {
    local file="$1"
    echo "  📏 Revisando líneas largas en $file"
    
    # Dividir líneas muy largas (más de 100 caracteres)
    # Esto es una aproximación, puede necesitar ajustes manuales
    awk 'length($0) > 100 && /^[^#]/ {
        # Si la línea es muy larga y no es comentario
        if (match($0, /^([^=]*=)/)) {
            # Si es una asignación, dividir después del =
            prefix = substr($0, 1, RSTART+RLENGTH-1)
            rest = substr($0, RSTART+RLENGTH)
            print prefix
            print "    " rest
        } else {
            # Para otras líneas, dividir en 80 caracteres
            print substr($0, 1, 80)
            print "    " substr($0, 81)
        }
    } {
        if (length($0) <= 100) print $0
    }' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

# Lista de archivos Python en scripts
FILES=(
    "scripts/bucket_manager.py"
    "scripts/config/setup_sqlite_connection.py"
    "scripts/explore_database.py"
    "scripts/explore_database_simple.py"
    "scripts/fix_format.py"
    "scripts/generar_datos_trafico.py"
    "scripts/gsutil_simulator.py"
    "scripts/monitoring/health_check.py"
)

# Procesar cada archivo
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "🔧 Procesando $file"
        clean_whitespace "$file"
        fix_long_lines "$file"
    else
        echo "⚠️  Archivo no encontrado: $file"
    fi
done

# Limpiar import no usado en bucket_manager.py
echo "🧹 Limpiando imports no usados..."
if [ -f "scripts/bucket_manager.py" ]; then
    # Comentar la línea del import no usado
    sed -i 's/^from datetime import datetime/# from datetime import datetime/' scripts/bucket_manager.py
fi

echo "✅ ¡Corrección completada!"
echo "🔍 Verificando resultados..."

# Verificar si flake8 está disponible
if command -v flake8 >/dev/null 2>&1; then
    echo "📊 Ejecutando flake8 en scripts..."
    flake8 scripts/ --max-line-length=100 --ignore=E203,W503 --exclude=__pycache__ || echo "⚠️  Algunos errores pueden persistir"
else
    echo "ℹ️  flake8 no disponible para verificación automática"
fi

echo "✨ ¡Proceso completado!"
