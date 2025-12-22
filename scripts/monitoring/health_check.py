#!/usr/bin/env python3
"""
Health Check del Sistema ETL de Tráfico Urbano
Verifica el estado de todos los componentes del sistema
"""
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
class HealthChecker:
    def __init__(self):
        self.db_path = "buckets/golden-bucket/database/trafico_urbano.db"
        self.airflow_ui_url = "http://localhost:8080"
    def check_database_health(self):
        """Verificar salud de la base de datos"""
        try:
            if not Path(self.db_path).exists():
                return {"status": "ERROR", "message": "Base de datos no encontrada"}
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Verificar tablas principales
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            if table_count == 0:
                return {"status": "ERROR", "message": "No hay tablas en la base de datos"}
            # Verificar datos en tablas principales
            main_tables = ['silver_sensores_trafico', 'golden_analisis_trafico']
            total_records = 0
            for table in main_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    total_records += count
                except sqlite3.OperationalError:
                    pass
            conn.close()
            if total_records == 0:
                return {"status": "WARNING", "message": "Base de datos vacía"}
            else:
                return {"status": "OK", "message": f"Base de datos saludable ({total_records} registros)"}
        except Exception as e:
            return {"status": "ERROR", "message": f"Error de base de datos: {str(e)}"}
    def check_airflow_health(self):
        """Verificar salud de Airflow"""
        try:
            # Verificar si Airflow está corriendo
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", self.airflow_ui_url],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip() == "200":
                return {"status": "OK", "message": "Airflow UI accesible"}
            else:
                return {"status": "WARNING", "message": "Airflow UI no accesible"}
        except subprocess.TimeoutExpired:
            return {"status": "ERROR", "message": "Timeout conectando a Airflow"}
        except Exception as e:
            return {"status": "ERROR", "message": f"Error verificando Airflow: {str(e)}"}
    def check_data_pipeline_health(self):
        """Verificar salud del pipeline de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Verificar datos recientes
            cursor.execute("""
                SELECT COUNT(*) FROM golden_analisis_trafico
                WHERE timestamp_analisis > datetime('now', '-1 hour')
            """)
            recent_data = cursor.fetchone()[0]
            conn.close()
            if recent_data > 0:
                return {"status": "OK", "message": f"Datos recientes encontrados ({recent_data} registros)"}
            else:
                return {"status": "WARNING", "message": "No hay datos recientes"}
        except Exception as e:
            return {"status": "ERROR", "message": f"Error verificando pipeline: {str(e)}"}
    def check_traffic_alerts(self):
        """Verificar alertas de tráfico"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Verificar sensores con alta congestión
            cursor.execute("""
                SELECT COUNT(*) FROM silver_sensores_trafico
                WHERE ocupacion_porcentaje > 80
            """)
            congested_sensors = cursor.fetchone()[0]
            # Verificar incidentes activos
            cursor.execute("""
                SELECT COUNT(*) FROM silver_incidentes_trafico
                WHERE estado = 'activo'
            """)
            active_incidents = cursor.fetchone()[0]
            conn.close()
            alerts = []
            if congested_sensors > 0:
                alerts.append(f"{congested_sensors} sensores con alta congestión")
            if active_incidents > 0:
                alerts.append(f"{active_incidents} incidentes activos")
            if alerts:
                return {"status": "WARNING", "message": f"Alertas de tráfico: {', '.join(alerts)}"}
            else:
                return {"status": "OK", "message": "No hay alertas de tráfico"}
        except Exception as e:
            return {"status": "ERROR", "message": f"Error al verificar alertas: {str(e)}"}
    def generate_report(self):
        """Genera reporte completo del sistema"""
        print("🔍 VERIFICACIÓN DE SALUD DEL SISTEMA ETL DE TRÁFICO URBANO")
        print("=" * 60)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        # Verificar base de datos
        print("🗄️ VERIFICANDO BASE DE DATOS...")
        db_health = self.check_database_health()
        status_icon = "✅" if db_health["status"] == "OK" else "⚠️" if db_health["status"] == "WARNING" else "❌"
        print(f"   {status_icon} {db_health['message']}")
        print()
        # Verificar Airflow
        print("🚀 VERIFICANDO AIRFLOW...")
        airflow_health = self.check_airflow_health()
        status_icon = "✅" if airflow_health["status"] == "OK" else "⚠️" if airflow_health["status"] == "WARNING" else "❌"
        print(f"   {status_icon} {airflow_health['message']}")
        print()
        # Verificar pipeline de datos
        print("📊 VERIFICANDO PIPELINE DE DATOS...")
        pipeline_health = self.check_data_pipeline_health()
        status_icon = "✅" if pipeline_health["status"] == "OK" else "⚠️" if pipeline_health["status"] == "WARNING" else "❌"
        print(f"   {status_icon} {pipeline_health['message']}")
        print()
        # Verificar alertas de tráfico
        print("🚨 VERIFICANDO ALERTAS DE TRÁFICO...")
        alerts_health = self.check_traffic_alerts()
        status_icon = "✅" if alerts_health["status"] == "OK" else "⚠️" if alerts_health["status"] == "WARNING" else "❌"
        print(f"   {status_icon} {alerts_health['message']}")
        print()
        # Resumen final
        all_checks = [db_health, airflow_health, pipeline_health, alerts_health]
        error_count = sum(1 for check in all_checks if check["status"] == "ERROR")
        warning_count = sum(1 for check in all_checks if check["status"] == "WARNING")
        print("📋 RESUMEN:")
        if error_count == 0 and warning_count == 0:
            print("   🎉 ¡Sistema completamente saludable!")
            return 0
        elif error_count == 0:
            print(f"   ⚠️ Sistema funcional con {warning_count} advertencias")
            return 1
        else:
            print(f"   ❌ Sistema con {error_count} errores y {warning_count} advertencias")
            return 2
def main():
    """Función principal"""
    try:
        checker = HealthChecker()
        exit_code = checker.generate_report()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(2)
if __name__ == "__main__":
    main()
