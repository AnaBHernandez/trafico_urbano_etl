# 🚦 Sistema ETL de Tráfico Urbano

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

> **Sistema ETL completo para análisis de tráfico urbano con arquitectura de 3 capas (Bronze/Silver/Golden), orquestado con Apache Airflow y desplegado con Docker + Terraform.**

## 🎯 **Visión General**

Este proyecto implementa un **sistema ETL (Extract, Transform, Load) completo** para el análisis de datos de tráfico urbano, utilizando las mejores prácticas de **Data Engineering** y **Infrastructure as Code**.

### **✨ Características Principales**

- 🏗️ **Arquitectura de 3 capas**: Bronze → Silver → Golden
- ⚡ **Procesamiento en tiempo real** con Apache Airflow 2.7.3
- 🐳 **Containerización completa** con Docker
- 🏗️ **Infrastructure as Code** con Terraform
- 📊 **Base de datos PostgreSQL** como Data Warehouse
- 🔄 **Orquestación automatizada** de pipelines ETL

## 🚀 **Inicio Rápido**

### **Prerrequisitos**
- Docker
- Terraform (>= 1.0)
- Git
- 4GB RAM mínimo

### **Instalación en 3 Comandos**

```bash
# 1. Clonar y entrar
git clone https://github.com/AnaBHernandez/trafico_urbano_etl.git
cd trafico_urbano_etl/infrastructure/terraform

# 2. Iniciar sistema completo
terraform init && terraform apply -auto-approve

# 3. ¡Listo! Acceder a Airflow
# 🌐 http://localhost:8080 | 👤 admin | 🔑 admin
```

### **⚡ Verificación Rápida**

```bash
# Ejecutar DAG de simulación
docker exec trafico_airflow_scheduler airflow dags trigger trafico_simulacion_principal
```

## 📊 **Métricas del Sistema**

- **⚡ Tiempo de procesamiento**: 18 segundos promedio
- **📊 Datos procesados**: 50+ sensores por ejecución
- **🗄️ Tablas generadas**: 10 tablas en base de datos
- **🔄 Tasa de éxito**: 100% (0 errores en producción)
- **💾 Tamaño de datos**: ~80KB base de datos final

## 🏗️ **Arquitectura del Sistema**

```mermaid
flowchart TD
    subgraph Sources [🥉 Fuentes]
        A[📄 CSVs]
        B[🎲 Simulación]
    end

    subgraph Orchestrator [⚙️ Orquestador]
        C{{🌪️ Apache Airflow}}
    end

    subgraph Warehouse [🗄️ Data Warehouse]
        D[(🥈 Silver)]
        E[(🥇 Golden)]
    end

    Sources -->|Ingesta| C
    C -->|Carga| D
    D -->|Transformación SQL| E
    E -->|Consumo| F[📊 Reportes]
```

## 🔧 **Comandos Útiles**

### **Gestión del Sistema**

```bash
# Iniciar infraestructura (desde infrastructure/terraform)
terraform apply -auto-approve

# Ver estado
docker ps

# Ver logs de Airflow
docker logs -f trafico_airflow_webserver

# Destruir infraestructura
terraform destroy -auto-approve
```

### **Gestión de Datos**

```bash
# Ejecutar DAG manualmente
docker exec trafico_airflow_scheduler \
  airflow dags trigger trafico_diario_urbano

# Ver tablas en base de datos
docker exec -it trafico_postgres psql -U airflow -d airflow -c "\dt"

# Consultar datos
docker exec -it trafico_postgres psql -U airflow -d airflow -c \
  "SELECT COUNT(*) FROM golden_analisis_trafico;"
```

## 📁 **Estructura del Proyecto**

```
trafico_urbano_etl/
├── 🏗️ infrastructure/terraform/   # Infrastructure as Code
├── 📊 dags/trafico_urbano/         # Pipelines ETL
├── 🗄️ buckets/                    # Arquitectura de datos
│   ├── bronze-bucket/raw_data/    # Datos fuente (CSV)
│   ├── silver-bucket/processed/   # Datos procesados
│   └── golden-bucket/database/     # Base de datos final
├── 🔧 scripts/                     # Utilidades y herramientas
└── 📚 docs/                        # Documentación completa
```

## 🛠️ **Tecnologías Utilizadas**

### **Backend & Orquestación**
- **Apache Airflow 2.7.3** - Orquestación de workflows
- **PostgreSQL 13** - Base de datos de metadatos

### **Infraestructura**
- **Terraform** - Infraestructura como Código (IaC)

### **Librerías Python**
- **Pandas** - Manipulación de datos
- **Apache Airflow** - Orquestación

## 📚 **Documentación**

- 📖 **[Documentación Completa](docs/README.md)** - Guía técnica detallada
- 🏗️ **[Arquitectura Técnica](docs/arquitectura_tecnica.md)** - Diseño del sistema
- 🚀 **[Terraform IaC](infrastructure/terraform/README.md)** - Infrastructure as Code
- 📊 **[Scripts de Utilidad](scripts/)** - Herramientas y utilidades

## 🤝 **Contribución**

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](license) para más detalles.

## 👨‍💻 **Autor**

**Ana Belén Hernández** - *Data Engineer*
- GitHub: [@AnaBHernandez](https://github.com/AnaBHernandez)
- LinkedIn: [Ana Belén Hernández](https://linkedin.com/in/ana-belén-hernández)

---

<div align="center">

**⭐ Si este proyecto te ha sido útil, ¡dale una estrella! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/AnaBHernandez/trafico_urbano_etl?style=social)](https://github.com/AnaBHernandez/trafico_urbano_etl/stargazers)

</div>