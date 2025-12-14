# Terraform para infraestructura local
# Equivalente a tu proyecto original de Google Cloud

terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Configuración del proveedor Docker
provider "docker" {
  # host = "npipe:////./pipe/docker_engine" # Descomentar para Windows
  host = "unix:///var/run/docker.sock"      # Estándar para Linux/Mac
}

# Imagen personalizada de Airflow (con Pandas)
resource "docker_image" "airflow_custom" {
  name = "trafico_airflow_custom:latest"
  build {
    context = "../.."
    dockerfile = "Dockerfile"
  }
}

# Red Docker para el proyecto
resource "docker_network" "trafico_network" {
  name = "trafico_urbano_network"
}

# Volumen para PostgreSQL
resource "docker_volume" "postgres_data" {
  name = "trafico_postgres_data"
}

# Contenedor PostgreSQL
resource "docker_container" "postgres" {
  name  = "trafico_postgres"
  image = "postgres:13"
  
  env = [
    "POSTGRES_USER=airflow",
    "POSTGRES_PASSWORD=airflow",
    "POSTGRES_DB=airflow"
  ]
  
  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }
  
  networks_advanced {
    name = docker_network.trafico_network.name
  }
  
  ports {
    internal = 5432
    external = 5432
  }
}

# Contenedor Airflow Webserver
resource "docker_container" "airflow_webserver" {
  name  = "trafico_airflow_webserver"
  image = docker_image.airflow_custom.name
  
  env = [
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow",
    "_AIRFLOW_WWW_USER_USERNAME=admin",
    "_AIRFLOW_WWW_USER_PASSWORD=admin"
  ]
  
  volumes {
    host_path      = abspath("${path.module}/../../dags")
    container_path = "/opt/airflow/dags"
  }
  
  volumes {
    host_path      = abspath("${path.module}/../../buckets")
    container_path = "/opt/airflow/buckets"
  }
  
  networks_advanced {
    name = docker_network.trafico_network.name
  }
  
  ports {
    internal = 8080
    external = 8080
  }
  
  depends_on = [docker_container.postgres]
}

# Contenedor Airflow Scheduler
resource "docker_container" "airflow_scheduler" {
  name  = "trafico_airflow_scheduler"
  image = docker_image.airflow_custom.name
  
  env = [
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow"
  ]
  
  volumes {
    host_path      = abspath("${path.module}/../../dags")
    container_path = "/opt/airflow/dags"
  }
  
  volumes {
    host_path      = abspath("${path.module}/../../buckets")
    container_path = "/opt/airflow/buckets"
  }
  
  networks_advanced {
    name = docker_network.trafico_network.name
  }
  
  depends_on = [docker_container.postgres]
}

# Outputs (equivalente a outputs.tf)
output "airflow_url" {
  value = "http://localhost:8080"
  description = "URL de acceso a Airflow"
}

output "postgres_connection" {
  value = "postgresql://airflow:airflow@localhost:5432/airflow"
  description = "Cadena de conexión a PostgreSQL"
}
