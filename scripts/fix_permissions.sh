#!/bin/bash
# Script para solucionar permisos de la base de datos SQLite

echo "🔧 Solucionando permisos de la base de datos SQLite..."

# Dar permisos completos a la base de datos
chmod 666 data/trafico_urbano.db

# Dar permisos completos al directorio de datos
chmod -R 777 data/

# Verificar permisos
echo "📊 Verificando permisos:"
ls -la data/trafico_urbano.db

echo "✅ Permisos solucionados correctamente"
