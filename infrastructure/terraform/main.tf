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
  force_remove = true
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
  image = "postgres:${var.postgres_version}"
  restart = "always"
  
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
    external = var.postgres_port
  }

  # Esperar a que Postgres esté listo antes de que otros servicios intenten conectar
  healthcheck {
    test         = ["CMD-SHELL", "pg_isready -U airflow"]
    interval     = "10s"
    retries      = 5
    start_period = "5s"
  }
}

# Contenedor para inicializar la base de datos de Airflow
# Este contenedor se ejecuta una vez, corre 'airflow db init' y termina.
resource "docker_container" "airflow_init_db" {
  name    = "trafico_airflow_init_db"
  image   = docker_image.airflow_custom.name
  restart = "no" # No queremos que se reinicie
  command = ["db", "init"]

  env = [
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres/airflow",
  ]

  networks_advanced {
    name = docker_network.trafico_network.name
  }

  # Depende de que Postgres esté saludable antes de intentar inicializar la BD
  depends_on = [docker_container.postgres]
}

# Contenedor Airflow Webserver
resource "docker_container" "airflow_webserver" {
  name  = "trafico_airflow_webserver"
  image = docker_image.airflow_custom.name
  restart = "always"
  command = ["webserver"]
  
  env = [
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres/airflow",
    "_AIRFLOW_WWW_USER_USERNAME=${var.airflow_admin_user}",
    "_AIRFLOW_WWW_USER_PASSWORD=${var.airflow_admin_password}",
    "AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql://airflow:airflow@trafico_postgres:5432/airflow",
    "AIRFLOW__CORE__FERNET_KEY=${var.airflow_fernet_key}",
    "AIRFLOW__WEBSERVER__SECRET_KEY=${var.airflow_webserver_secret_key}",
    "DATA_WAREHOUSE_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres:5432/airflow",
    "AIRFLOW__CORE__LOAD_EXAMPLES=False"
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
    external = var.airflow_port
  }
  
  # Depende de que la BD haya sido inicializada
  depends_on = [docker_container.airflow_init_db]
}

# Contenedor Airflow Scheduler
resource "docker_container" "airflow_scheduler" {
  name  = "trafico_airflow_scheduler"
  image = docker_image.airflow_custom.name
  restart = "always"
  command = ["scheduler"]
  
  env = [
    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres/airflow",
    "AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql://airflow:airflow@trafico_postgres:5432/airflow",
    "AIRFLOW__CORE__FERNET_KEY=${var.airflow_fernet_key}",
    "AIRFLOW__WEBSERVER__SECRET_KEY=${var.airflow_webserver_secret_key}",
    "DATA_WAREHOUSE_CONN=postgresql+psycopg2://airflow:airflow@trafico_postgres:5432/airflow",
    "AIRFLOW__CORE__LOAD_EXAMPLES=False"
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
  
  # Depende de que la BD haya sido inicializada
  depends_on = [docker_container.airflow_init_db]
}

# Outputs (equivalente a outputs.tf)
output "airflow_url" {
  value = "http://localhost:${var.airflow_port}"
  description = "URL de acceso a Airflow"
}

output "postgres_connection" {
  value = "postgresql://airflow:airflow@localhost:${var.postgres_port}/airflow"
  description = "Cadena de conexión a PostgreSQL"
}

output "airflow_admin_credentials" {
  description = "Credenciales de administrador de Airflow"
  value = {
    username = var.airflow_admin_user
    password = var.airflow_admin_password
  }
  sensitive = true
}

output "docker_network_name" {
  description = "Nombre de la red Docker"
  value       = docker_network.trafico_network.name
}

output "postgres_volume_name" {
  description = "Nombre del volumen de PostgreSQL"
  value       = docker_volume.postgres_data.name
}
