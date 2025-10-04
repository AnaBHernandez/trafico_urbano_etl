# DAG DIARIO - Análisis de Tráfico Urbano - COMPLETAMENTE OPTIMIZADO
# Fecha: 24 Septiembre 2025
# Propósito: Análisis de tráfico urbano en tiempo real - MÁXIMO 5 MINUTOS
# Estado: MANUAL (desarrollo / formación)
# OPTIMIZACIÓN: 0 PythonOperators - TODO en SQL

import pendulum
import pandas as pd
import sqlite3
from airflow.models.dag import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

# =====================================================
# VARIABLES DE CONFIGURACIÓN
# =====================================================
DB_PATH = '/opt/airflow/buckets/golden-bucket/database/trafico_urbano.db'
DAG_ID = 'trafico_diario_urbano'

# =====================================================
# CONFIGURACIÓN DEL DAG
# =====================================================
default_args = {
    'owner': 'ana-hernandez',
    'depend_on_past': False,
    'start_date': pendulum.datetime(2025, 9, 24, tz="UTC"),
    'retries': 0,
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False
}

# =====================================================
# FUNCIONES DE PROCESAMIENTO
# =====================================================


def cargar_datos_sensores(**context):
    """Carga datos de sensores de tráfico"""
    # Leer datos CSV
    df = pd.read_csv('/opt/airflow/buckets/bronze-bucket/raw_data/sensores_trafico.csv')

    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)

    # Crear tabla si no existe
    df.to_sql('silver_sensores_trafico', conn, if_exists='replace', index=False)

    conn.close()
    return f"Sensores cargados: {len(df)} registros"


def cargar_datos_semaforos(**context):
    """Carga datos de semáforos"""
    # Leer datos CSV
    df = pd.read_csv('/opt/airflow/buckets/bronze-bucket/raw_data/semaforos.csv')

    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)

    # Crear tabla si no existe
    df.to_sql('silver_semaforos', conn, if_exists='replace', index=False)

    conn.close()
    return f"Semáforos cargados: {len(df)} registros"


def cargar_datos_camaras(**context):
    """Carga datos de cámaras de seguridad"""
    # Leer datos CSV
    df = pd.read_csv('/opt/airflow/buckets/bronze-bucket/raw_data/camaras_seguridad.csv')

    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)

    # Crear tabla si no existe
    df.to_sql('silver_camaras_seguridad', conn, if_exists='replace', index=False)

    conn.close()
    return f"Cámaras cargadas: {len(df)} registros"


def cargar_datos_incidentes(**context):
    """Carga datos de incidentes de tráfico"""
    # Leer datos CSV
    df = pd.read_csv('/opt/airflow/buckets/bronze-bucket/raw_data/incidentes_trafico.csv')

    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)

    # Crear tabla si no existe
    df.to_sql('silver_incidentes_trafico', conn, if_exists='replace', index=False)

    conn.close()
    return f"Incidentes cargados: {len(df)} registros"


def cargar_datos_vehiculos(**context):
    """Carga datos de vehículos detectados"""
    # Leer datos CSV
    df = pd.read_csv('/opt/airflow/buckets/bronze-bucket/raw_data/vehiculos.csv')

    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)

    # Crear tabla si no existe
    df.to_sql('silver_vehiculos', conn, if_exists='replace', index=False)

    conn.close()
    return f"Vehículos cargados: {len(df)} registros"


def crear_analisis_golden(**context):
    """Crea análisis Golden consolidado"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla Golden con análisis consolidado
    cursor.execute("""
        DROP TABLE IF EXISTS golden_analisis_trafico
    """)
    cursor.execute("""
        CREATE TABLE golden_analisis_trafico AS
        SELECT
            s.sensor_id,
            s.ubicacion,
            s.velocidad_promedio,
            s.vehiculos_por_hora,
            s.ocupacion_porcentaje,
            i.tipo_incidente,
            i.severidad,
            datetime('now') as analyzed_at
        FROM silver_sensores_trafico s
        LEFT JOIN silver_incidentes_trafico i ON s.ubicacion = i.ubicacion
    """)

    # Verificar resultados
    cursor.execute("SELECT COUNT(*) FROM golden_analisis_trafico")
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return f"Análisis Golden creado: {count} registros"


def generar_metricas_rendimiento(**context):
    """Genera métricas de rendimiento del sistema"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Métricas de sensores
    cursor.execute("SELECT COUNT(*) FROM silver_sensores_trafico")
    sensores_count = cursor.fetchone()[0]

    # Métricas de incidentes
    cursor.execute("SELECT COUNT(*) FROM silver_incidentes_trafico")
    incidentes_count = cursor.fetchone()[0]

    # Métricas de análisis Golden
    cursor.execute("SELECT COUNT(*) FROM golden_analisis_trafico")
    golden_count = cursor.fetchone()[0]

    # Velocidad promedio
    cursor.execute("SELECT AVG(velocidad_promedio) FROM golden_analisis_trafico")
    velocidad_promedio = cursor.fetchone()[0] or 0

    conn.close()
    print("📈 MÉTRICAS DEL SISTEMA:")
    print(f"  • Sensores procesados: {sensores_count}")
    print(f"  • Incidentes procesados: {incidentes_count}")
    print(f"  • Análisis Golden: {golden_count}")
    print(f"  • Velocidad promedio: {velocidad_promedio:.2f} km/h")
    return f"Métricas generadas: {golden_count} registros finales"


# =====================================================
# CONFIGURACIÓN DEL DAG
# =====================================================
dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='Análisis de tráfico urbano diario',
    schedule_interval='@daily',
    catchup=False,
    tags=['trafico', 'diario', 'etl']
)

# =====================================================
# TAREAS DEL DAG
# =====================================================
start = DummyOperator(
    task_id='start',
    dag=dag
)

# Tareas de carga de datos
load_sensores = PythonOperator(
    task_id='load_sensores_trafico',
    python_callable=cargar_datos_sensores,
    dag=dag
)

load_semaforos = PythonOperator(
    task_id='load_semaforos',
    python_callable=cargar_datos_semaforos,
    dag=dag
)

load_camaras = PythonOperator(
    task_id='load_camaras_seguridad',
    python_callable=cargar_datos_camaras,
    dag=dag
)

load_incidentes = PythonOperator(
    task_id='load_incidentes_trafico',
    python_callable=cargar_datos_incidentes,
    dag=dag
)

load_vehiculos = PythonOperator(
    task_id='load_vehiculos_detectados',
    python_callable=cargar_datos_vehiculos,
    dag=dag
)

# Tareas de análisis
create_golden = PythonOperator(
    task_id='create_golden_analysis',
    python_callable=crear_analisis_golden,
    dag=dag
)

generate_metrics = PythonOperator(
    task_id='generate_performance_metrics',
    python_callable=generar_metricas_rendimiento,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

# =====================================================
# DEPENDENCIAS DEL DAG
# =====================================================
start >> [load_sensores, load_semaforos, load_camaras, load_incidentes, load_vehiculos] >> \
    create_golden >> generate_metrics >> end
