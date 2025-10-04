# Outputs para Terraform local
# Equivalente a outputs.tf de tu proyecto original

output "airflow_ui_url" {
  description = "URL de acceso a la interfaz de Airflow"
  value       = "http://localhost:${var.airflow_port}"
}

output "postgres_connection_string" {
  description = "Cadena de conexión a PostgreSQL"
  value       = "postgresql://airflow:airflow@localhost:${var.postgres_port}/airflow"
  sensitive = true
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
