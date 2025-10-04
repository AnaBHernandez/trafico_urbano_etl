#!/usr/bin/env python3
"""
Configuración de conexión SQLite para Airflow
Crea la base de datos y tablas necesarias
"""
import sqlite3
from pathlib import Path
def setup_sqlite_connection():
    """Configura la conexión SQLite para Airflow"""
    # Crear directorio de datos si no existe
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    # Crear base de datos SQLite
    db_path = data_dir / "trafico_urbano.db"
    print(f"🗄️ Creando base de datos SQLite en: {db_path}")
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Crear tablas si no existen
    print("📊 Creando tablas de la capa Silver...")
    # Tabla de sensores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_sensores_trafico (
            sensor_id TEXT PRIMARY KEY,
            ubicacion TEXT,
            tipo_sensor TEXT,
            estado TEXT,
            ultima_lectura TEXT,
            velocidad_promedio REAL,
            ocupacion_porcentaje REAL,
            timestamp_creacion TEXT
        )
    """)
    # Tabla de vehículos detectados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_vehiculos_detectados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            tipo_vehiculo TEXT,
            velocidad REAL,
            timestamp TEXT,
            ubicacion TEXT,
            FOREIGN KEY (sensor_id) REFERENCES silver_sensores_trafico(sensor_id)
        )
    """)
    # Tabla de incidentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_incidentes_trafico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ubicacion TEXT,
            tipo_incidente TEXT,
            severidad TEXT,
            timestamp TEXT,
            descripcion TEXT,
            estado TEXT
        )
    """)
    # Tabla de cámaras de seguridad
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_camaras_seguridad (
            camara_id TEXT PRIMARY KEY,
            ubicacion TEXT,
            estado TEXT,
            ultima_verificacion TEXT,
            resolucion TEXT,
            tipo_camara TEXT
        )
    """)
    # Tabla de semáforos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_semaforos (
            semaforo_id TEXT PRIMARY KEY,
            ubicacion TEXT,
            estado TEXT,
            ultimo_cambio TEXT,
            tipo_control TEXT,
            sincronizacion TEXT
        )
    """)
    print("📊 Creando tablas de la capa Golden...")
    # Tabla de análisis consolidado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS golden_analisis_trafico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ubicacion TEXT,
            fecha TEXT,
            hora TEXT,
            velocidad_promedio REAL,
            ocupacion_porcentaje REAL,
            incidentes_count INTEGER,
            vehiculos_count INTEGER,
            congestion_nivel TEXT,
            recomendaciones TEXT,
            timestamp_analisis TEXT
        )
    """)
    # Tabla de métricas de rendimiento
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS golden_metricas_rendimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ubicacion TEXT,
            periodo TEXT,
            velocidad_promedio REAL,
            tiempo_viaje_promedio REAL,
            nivel_congestion REAL,
            eficiencia_trafico REAL,
            timestamp_metricas TEXT
        )
    """)
    # Crear índices para mejorar rendimiento
    print("🔍 Creando índices...")
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_silver_sensores_ubicacion ON silver_sensores_trafico(ubicacion)",
        "CREATE INDEX IF NOT EXISTS idx_silver_vehiculos_sensor ON silver_vehiculos_detectados(sensor_id)",
        "CREATE INDEX IF NOT EXISTS idx_silver_vehiculos_timestamp ON silver_vehiculos_detectados(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_golden_analisis_ubicacion ON golden_analisis_trafico(ubicacion)",
        "CREATE INDEX IF NOT EXISTS idx_golden_analisis_fecha ON golden_analisis_trafico(fecha)",
        "CREATE INDEX IF NOT EXISTS idx_golden_metricas_ubicacion ON golden_metricas_rendimiento(ubicacion)"
    ]
    for indice in indices:
        cursor.execute(indice)
    # Confirmar cambios
    conn.commit()
    print("✅ Base de datos SQLite configurada correctamente")
    # Mostrar información de las tablas creadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print(f"📋 Tablas creadas: {len(tablas)}")
    for tabla in tablas:
        print(f"  - {tabla[0]}")
    conn.close()
    return str(db_path)
def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        db_path = setup_sqlite_connection()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Probar consulta simple
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Conexión exitosa. {count} tablas encontradas.")
        return True
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")
        return False
if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DE BASE DE DATOS SQLITE")
    print("=" * 50)
    if test_connection():
        print("\n🎉 ¡Configuración completada exitosamente!")
    else:
        print("\n❌ Error en la configuración")
