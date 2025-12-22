#!/bin/bash
# Script de instalación de Docker Engine en Ubuntu
# Basado en la documentación oficial y bitácora de ingeniería

set -e # Detener script si hay errores

echo "🔄 Actualizando sistema y dependencias..."
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

echo "🔑 Añadiendo clave GPG oficial de Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "📦 Configurando repositorio estable..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "⬇️ Instalando Docker Engine..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

echo "👤 Configurando usuario actual para usar Docker sin sudo..."
sudo usermod -aG docker $USER

echo "✅ ¡Instalación completada! Por favor, cierra sesión y vuelve a entrar para aplicar los cambios de grupo."