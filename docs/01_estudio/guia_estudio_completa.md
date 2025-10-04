# 📚 guía de estudio completa - sistema etl de tráfico urbano

## 🎯 objetivo del proyecto
sistema etl completo para análisis de tráfico urbano con apache airflow, docker y arquitectura de datos en capas.

## 🏗️ arquitectura general

### diagrama de alto nivel
```
┌─────────────────────────────────────────────────────────────────┐
│                    capa de presentación                        │
├─────────────────────────────────────────────────────────────────┤
│  🌐 airflow web ui (puerto 8080)                              │
│  📊 dashboards y visualizaciones                              │
│  🔍 monitoreo y logs                                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    capa de orquestación                       │
├─────────────────────────────────────────────────────────────────┤
│  🚦 apache airflow 2.7.3                                     │
│  ├── dag diario (trafico_diario_urbano)                      │
│  ├── dag histórico (trafico_historico_urbano)                │
│  └── dag principal (trafico_principal)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    capa de procesamiento                      │
├─────────────────────────────────────────────────────────────────┤
│  🐍 python 3.8+                                              │
│  ├── operadores personalizados                               │
│  ├── funciones de transformación                             │
│  ├── validación de datos                                     │
│  └── generación de métricas                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    capa de almacenamiento                      │
├─────────────────────────────────────────────────────────────────┤
│  🗄️ sqlite database                                          │
│  ├── tablas silver (datos procesados)                        │
│  ├── tablas golden (análisis consolidados)                   │
│  └── índices y optimizaciones                                │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 componentes del sistema

### 1. apache airflow
- **versión**: 2.7.3
- **configuración**: localexecutor
- **base de datos**: postgresql 13
- **puerto**: 8080
- **autenticación**: admin/admin

### 2. base de datos
- **tipo**: sqlite (local)
- **ubicación**: `/opt/airflow/data/trafico_urbano.db`
- **tamaño**: ~65kb
- **tablas**: 9 tablas (silver + golden)

### 3. contenedores docker
```yaml
services:
  postgres:          # base de datos de airflow
  airflow-init:      # inicialización
  airflow-webserver: # interfaz web
  airflow-scheduler: # ejecutor de dags
```

## 📊 flujo de datos

### pipeline bronze → silver → golden

#### 1. capa bronze (datos crudos)
```python
# fuentes de datos
- archivos csv (sensores_trafico.csv)
- apis externas (kaggle, openstreetmap)
- datos en tiempo real (simulados)
- archivos de configuración

# procesamiento
- validación de formato
- limpieza básica
- almacenamiento en bronze bucket
```

#### 2. capa silver (datos procesados)
```python
# transformaciones
- enriquecimiento de datos
- validación de reglas de negocio
- normalización de formatos
- cálculo de métricas básicas

# almacenamiento
- tablas sqlite (silver_*)
- silver bucket
- índices para consultas rápidas
```

#### 3. capa golden (análisis)
```python
# análisis consolidados
- métricas de tráfico
- alertas de congestión
- tendencias históricas
- reportes ejecutivos

# almacenamiento
- tablas golden (golden_*)
- golden bucket
- backups automáticos
```

## 🛠️ tecnologías utilizadas

### backend
- **python 3.8+**: lógica de negocio
- **apache airflow 2.7.3**: orquestación
- **sqlite**: base de datos local
- **pandas**: manipulación de datos
- **sqlalchemy**: orm para consultas

### infraestructura
- **docker**: containerización
- **docker compose**: orquestación de servicios
- **postgresql 13**: metadatos de airflow
- **linux**: sistema operativo base

### herramientas de desarrollo
- **git**: control de versiones
- **vs code**: editor de código
- **docker desktop**: gestión de contenedores
- **sqlite browser**: exploración de bd

## 🎨 patrones de diseño

### 1. patrón etl (extraer, transformar, cargar)
```python
# extraer
def extraer_datos():
    # extraer datos de fuentes
    pass

# transformar
def transformar_datos():
    # transformar y limpiar datos
    pass

# cargar
def cargar_datos():
    # cargar datos procesados
    pass
```

### 2. patrón de capas (arquitectura en capas)
- **capa de presentación**: airflow ui
- **capa de lógica**: dags y operadores
- **capa de datos**: sqlite + buckets
- **capa de infraestructura**: docker

### 3. patrón de buckets (data lake)
```
bronze bucket  →  silver bucket  →  golden bucket
   (crudo)         (procesado)       (análisis)
```

### 4. patrón de orquestación (workflow)
```python
# dependencias entre tareas
tarea1 >> tarea2 >> tarea3
tarea1 >> tarea4
[tarea2, tarea4] >> tarea5
```

## 📈 escalabilidad

### escalabilidad horizontal
- **múltiples workers**: airflow puede escalar workers
- **distribución de dags**: diferentes dags en diferentes workers
- **paralelización**: tareas independientes en paralelo

### escalabilidad vertical
- **recursos docker**: aumentar cpu/ram de contenedores
- **base de datos**: migrar a postgresql/mysql
- **almacenamiento**: aumentar espacio de discos

### escalabilidad de datos
- **particionamiento**: dividir datos por fecha/ubicación
- **índices**: optimizar consultas frecuentes
- **caché**: implementar redis para consultas repetitivas

## 🔒 seguridad

### autenticación
- **airflow**: usuario/contraseña básica
- **base de datos**: acceso local únicamente
- **docker**: contenedores aislados

### autorización
- **roles**: admin, dag creator, viewer
- **permisos**: por dag y por tarea
- **auditoría**: logs de ejecución

### protección de datos
- **encriptación**: datos en tránsito (https)
- **backups**: respaldo automático de datos críticos
- **retención**: políticas de limpieza de logs

## 📊 monitoreo y observabilidad

### métricas del sistema
- **dags**: estado, duración, éxito/fallo
- **tareas**: tiempo de ejecución, recursos utilizados
- **base de datos**: tamaño, consultas, rendimiento
- **buckets**: archivos, tamaño, transferencias

### logs
- **airflow**: logs de dags y tareas
- **docker**: logs de contenedores
- **aplicación**: logs de python

### alertas
- **fallos de dag**: notificaciones automáticas
- **congestión**: alertas de tráfico crítico
- **recursos**: uso de cpu/memoria
- **datos**: calidad y completitud

## 🚀 rendimiento

### optimizaciones implementadas
- **índices sqlite**: consultas rápidas
- **paralelización**: tareas independientes
- **caché**: datos frecuentemente accedidos
- **limpieza**: archivos temporales automáticos

### métricas de rendimiento
- **dag diario**: ~2-3 minutos
- **dag histórico**: ~1-2 minutos
- **dag principal**: ~2-3 minutos
- **total**: ~5-8 minutos para todos los dags

### límites actuales
- **sensores**: 50 sensores simultáneos
- **datos**: ~1mb por día
- **consultas**: <100ms promedio
- **concurrencia**: 3 dags simultáneos

## 🎯 conceptos clave para estudiar

### 1. etl (extraer, transformar, cargar)
- **extraer**: extraer datos de fuentes heterogéneas
- **transformar**: limpiar, validar y enriquecer datos
- **cargar**: cargar datos procesados en destino

### 2. arquitectura de datos
- **capa bronze**: datos crudos sin procesar
- **capa silver**: datos limpios y estructurados
- **capa golden**: datos listos para análisis

### 3. orquestación de workflows
- **dags**: directed acyclic graphs
- **tareas**: unidades de trabajo
- **operadores**: tipos de tareas
- **dependencias**: dependencias entre tareas

### 4. containerización
- **docker**: contenedores ligeros
- **docker compose**: orquestación de servicios
- **volúmenes**: persistencia de datos
- **redes**: comunicación entre contenedores

## 📝 comandos esenciales

### docker
```bash
# iniciar servicios
docker-compose up -d

# ver estado
docker-compose ps

# ver logs
docker-compose logs -f

# parar servicios
docker-compose down
```

### airflow
```bash
# listar dags
docker-compose exec airflow-webserver airflow dags list

# ejecutar dag
docker-compose exec airflow-webserver airflow dags trigger trafico_principal

# ver estado
docker-compose exec airflow-webserver airflow dags state trafico_principal 2025-10-02
```

### base de datos
```bash
# verificar registros
python3 -c "import sqlite3; conn = sqlite3.connect('data/trafico_urbano.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM golden_analisis_trafico'); print(f'Registros: {cursor.fetchone()[0]}'); conn.close()"
```

## 🎓 preguntas de estudio

### nivel básico
1. ¿qué es un sistema etl?
2. ¿cuáles son las 3 capas de la arquitectura de datos?
3. ¿qué es apache airflow?
4. ¿para qué sirve docker?

### nivel intermedio
1. ¿cómo funciona el patrón bronze → silver → golden?
2. ¿qué son los dags en airflow?
3. ¿cómo se implementa la orquestación de tareas?
4. ¿qué ventajas tiene la containerización?

### nivel avanzado
1. ¿cómo optimizarías el rendimiento del sistema?
2. ¿qué estrategias de escalabilidad implementarías?
3. ¿cómo migrarías a un entorno de producción?
4. ¿qué métricas de monitoreo son más importantes?

## 🚀 próximos pasos

### para estudiar
1. **revisar código**: examinar los dags y scripts
2. **experimentar**: modificar parámetros y ver resultados
3. **documentar**: anotar conceptos nuevos
4. **practicar**: crear nuevos dags simples

### para linkedin
1. **capturar evidencia**: screenshots del sistema funcionando
2. **documentar logros**: métricas y resultados
3. **preparar presentación**: explicar el proyecto técnicamente
4. **actualizar perfil**: agregar tecnologías y logros

---

**📝 guía de estudio actualizada: octubre 2025**
**👩‍💻 autor: ana belén hernández**
**🏷️ versión: 1.0.0**
