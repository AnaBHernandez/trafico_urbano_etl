# Dockerfile simplificado para el sistema ETL de tráfico urbano
FROM python:3.8-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p data logs

# Comando por defecto
CMD ["python", "-c", "print('Sistema ETL de Tráfico Urbano - Docker container iniciado correctamente')"]
