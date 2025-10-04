# 🏗️ **TERRAFORM PARA INFRAESTRUCTURA LOCAL**

**Gestión de infraestructura local con Terraform (equivalente a tu proyecto original de Google Cloud)**

---

## 🎯 **EQUIVALENCIAS CON TU PROYECTO ORIGINAL**

### **ANTES (Google Cloud + Terraform):**
```bash
# Tu proyecto original
terraform init
terraform plan
terraform apply
```

### **AHORA (Docker Local + Terraform):**
```bash
# Mismos comandos, infraestructura local
terraform init
terraform plan
terraform apply
```

---

## 🚀 **COMANDOS TERRAFORM**

### **INICIALIZAR:**
```bash
cd infrastructure/terraform
terraform init
```

### **PLANIFICAR:**
```bash
terraform plan
```

### **APLICAR:**
```bash
terraform apply
```

### **DESTRUIR:**
```bash
terraform destroy
```

---

## 📊 **RECURSOS CREADOS**

### **DOCKER:**
- **Red:** `trafico_urbano_network`
- **Volumen:** `trafico_postgres_data`
- **Contenedores:**
  - `trafico_postgres` (PostgreSQL)
  - `trafico_airflow_webserver` (Airflow UI)
  - `trafico_airflow_scheduler` (Airflow Scheduler)

### **PUERTOS:**
- **Airflow:** http://localhost:8080
- **PostgreSQL:** localhost:5432

---

## 🔧 **CONFIGURACIÓN**

### **VARIABLES:**
- `project_name`: Nombre del proyecto
- `airflow_version`: Versión de Airflow
- `postgres_version`: Versión de PostgreSQL
- `airflow_port`: Puerto de Airflow
- `postgres_port`: Puerto de PostgreSQL

### **OUTPUTS:**
- `airflow_ui_url`: URL de Airflow
- `postgres_connection_string`: Conexión a PostgreSQL
- `airflow_admin_credentials`: Credenciales de admin

---

## 🎯 **VENTAJAS DE TERRAFORM LOCAL**

### **✅ BENEFICIOS:**
- **Mismos comandos** que tu proyecto original
- **Gestión declarativa** de infraestructura
- **Versionado** de configuración
- **Estado** de infraestructura
- **Reutilizable** en otros proyectos

### **⚠️ CONSIDERACIONES:**
- **Más complejo** que Docker Compose
- **Requiere** Terraform instalado
- **Estado local** (no compartido)

---

## 🚀 **COMPARACIÓN: DOCKER COMPOSE vs TERRAFORM**

| **Aspecto** | **Docker Compose** | **Terraform** |
|-------------|-------------------|---------------|
| **Simplicidad** | ✅ Muy simple | ⚠️ Más complejo |
| **Comandos** | `docker-compose up` | `terraform apply` |
| **Estado** | ❌ No persistente | ✅ Persistente |
| **Versionado** | ⚠️ Básico | ✅ Avanzado |
| **Reutilización** | ⚠️ Limitada | ✅ Alta |
| **Aprendizaje** | ✅ Fácil | ⚠️ Curva de aprendizaje |

---

## 🎯 **RECOMENDACIÓN**

### **PARA DESARROLLO RÁPIDO:**
```bash
# Usar Docker Compose (más simple)
docker-compose up -d
```

### **PARA PRODUCCIÓN/ESCALABILIDAD:**
```bash
# Usar Terraform (más robusto)
cd infrastructure/terraform
terraform apply
```

---

**💡 CONCLUSIÓN:** Tienes **AMBAS OPCIONES** disponibles:
- **Docker Compose** para desarrollo rápido
- **Terraform** para gestión profesional de infraestructura

**¡Elige la que prefieras según tus necesidades!** 🚀
