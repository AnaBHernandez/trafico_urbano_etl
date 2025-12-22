# 📝 Bitácora de Ingeniería: Configuración y Migración

**Fecha:** 14 de Diciembre 2025
**Contexto:** Preparación de entorno local para entrevista técnica (Data Engineer).

## 1. 🛠️ Troubleshooting: Docker en Windows

### Problema
Docker Desktop y WSL2 se quedaban bloqueados ("unresponsive"), impidiendo la ejecución de `docker-compose` y generando errores de conexión con el daemon.

### Solución Aplicada
Se utilizaron comandos de PowerShell para forzar el reinicio del subsistema Linux (WSL) y limpiar procesos zombies:

```powershell
# Reinicio forzado de WSL
taskkill /F /IM "wsl.exe"
wsl --shutdown
```

## 2. 🏗️ Infraestructura como Código (Terraform)

### Desafío
Terraform fallaba al intentar construir la imagen de Docker personalizada debido a cómo Windows maneja las rutas absolutas (barras invertidas `\` vs `/`).

### Solución
Se modificó el archivo `main.tf` para utilizar rutas relativas en el contexto de construcción, lo cual es compatible tanto con Windows como con Linux:

```hcl
  build {
    context = "../.."  # Ruta relativa en lugar de abspath()
    dockerfile = "Dockerfile"
  }
```

## 3. 🎨 Portfolio Técnico
Se desarrolló un archivo `portfolio.html` independiente para presentar el proyecto de forma visual en caso de no poder realizar la demo técnica en vivo. Incluye diagramas de arquitectura (Mermaid.js) y métricas de negocio.

## 4. 🐧 Decisión de Migración a Linux

**Decisión:** Migrar el entorno de desarrollo de Windows a Linux (Ubuntu).

**Justificación Técnica:**
1.  **Estándar de Industria:** La mayoría de infraestructuras de datos (Cloud) corren sobre Linux.
2.  **Rendimiento:** Docker es nativo en Linux, eliminando la sobrecarga de virtualización de WSL2.
3.  **Estabilidad:** Se eliminan los errores de "path separators" y bloqueos de interfaz gráfica.

**Acciones Realizadas:**
1.  Ajuste de `main.tf` para usar el socket unix (`unix:///var/run/docker.sock`).
2.  Commit y Push de todo el código a GitHub.
3.  Instrucciones de despliegue en Linux (`git clone` + `docker-compose up`).

## 5. ✅ Verificación de Compatibilidad Linux

**Análisis de Portabilidad:**

1.  **Rutas de Archivos:** El uso de `abspath("${path.module}/../../dags")` en el código de Terraform (visible en el Portfolio) funcionará nativamente en Linux, resolviendo rutas absolutas tipo `/home/ana-hernandez/...` sin problemas de barras invertidas (`\`).
2.  **Docker Socket:** Al usar Linux, el provider de Docker debe configurarse con `host = "unix:///var/run/docker.sock"`, lo cual es el estándar y más estable que la conexión TCP de Windows.
3.  **Portfolio Web:** El archivo `portfolio.html` es agnóstico al sistema operativo y se visualizará correctamente en navegadores Linux (Firefox/Chrome).

**Comando de Validación Rápida:**
```bash
# Verificar que Docker corre nativamente y tiene acceso a volúmenes
docker run --rm -v $(pwd):/data alpine ls -la /data
```