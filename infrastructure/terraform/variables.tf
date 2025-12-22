# Variables para Terraform local
# Equivalente a variables.tf de tu proyecto original

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "trafico_urbano_etl"
}

variable "airflow_version" {
  description = "Versión de Airflow"
  type        = string
  default     = "2.7.3"
}

variable "postgres_version" {
  description = "Versión de PostgreSQL"
  type        = string
  default     = "13"
}

variable "airflow_port" {
  description = "Puerto para Airflow"
  type        = number
  default     = 8080
}

variable "postgres_port" {
  description = "Puerto para PostgreSQL"
  type        = number
  default     = 5432
}

variable "airflow_admin_user" {
  description = "Usuario administrador de Airflow"
  type        = string
  default     = "admin"
}

variable "airflow_admin_password" {
  description = "Contraseña del administrador de Airflow"
  type        = string
  default     = "admin"
  sensitive   = true
}

variable "airflow_fernet_key" {
  description = "Clave Fernet para encriptación en Airflow (debe ser base64 url-safe de 32 bytes)"
  type        = string
  default     = "46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=" # Clave estática para dev
}

variable "airflow_webserver_secret_key" {
  description = "Clave secreta para firmar cookies y comunicación interna en Airflow"
  type        = string
  default     = "clave_secreta_fija_para_desarrollo_local"
}
