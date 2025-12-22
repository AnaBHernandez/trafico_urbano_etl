#!/bin/bash
# Script de instalación de Terraform en Ubuntu
# Basado en la documentación oficial de HashiCorp

set -e

echo "🔄 Actualizando dependencias..."
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl wget

echo "🔑 Añadiendo clave GPG de HashiCorp..."
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

echo "📦 Añadiendo repositorio oficial de HashiCorp..."
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

echo "⬇️ Instalando Terraform..."
sudo apt-get update
sudo apt-get install -y terraform

echo "✅ ¡Instalación completada!"
terraform -version