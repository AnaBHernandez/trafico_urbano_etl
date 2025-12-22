# DAG DIARIO - Análisis de Tráfico Urbano - ARQUITECTURA ELT (Simulación Cloud)
# Fecha: 24 Septiembre 2025
# Propósito: Replicar arquitectura Tecnología AB (Bronze -> Silver -> Golden)
# Estrategia: ELT con PostgreSQL (Simulando BigQuery)

import os
import pendulum
from pathlib import Path
from airflow.models.dag import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Intent: Hacer rutas configurables por variables de entorno y defensivas
try:
    import pandas as pd
except Exception as e:
    pd = None

# =====================================================
# VARIABLES DE CONFIGURACIÓN
# =====================================================
# Rutas configurables: si Airflow monta /opt/airflow se usarán, si no, usamos rutas del repo
DEFAULT_BRONZE = Path(os.environ.get('BRONZE_PATH', Path.cwd() / 'buckets' / 'bronze-bucket' / 'raw_data'))
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

def cargar_csv_a_postgres(table_name, csv_filename, **context):
    """
    Simula GCSToBigQuery: Lee CSV (Bronze) y carga a Postgres (Silver).
    Usa PostgresHook para manejar la conexión.
    """
    if pd is None:
        raise RuntimeError("pandas es necesario para la carga inicial")

    csv_path = DEFAULT_BRONZE / csv_filename
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    
    # Usar el Hook de Postgres para obtener el engine de SQLAlchemy
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    engine = pg_hook.get_sqlalchemy_engine()

    # Carga a Postgres (Silver Layer)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    return f"Cargado {table_name}: {len(df)} registros"


def generar_metricas_rendimiento(**context):
    """Genera métricas de rendimiento del sistema"""
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
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
    tags=['trafico', 'diario', 'elt', 'postgres']
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
    python_callable=cargar_csv_a_postgres,
    op_kwargs={'table_name': 'silver_sensores_trafico', 'csv_filename': 'sensores_trafico.csv'},
    dag=dag
)

load_semaforos = PythonOperator(
    task_id='load_semaforos',
    python_callable=cargar_csv_a_postgres,
    op_kwargs={'table_name': 'silver_semaforos', 'csv_filename': 'semaforos.csv'},
    dag=dag
)

load_camaras = PythonOperator(
    task_id='load_camaras_seguridad',
    python_callable=cargar_csv_a_postgres,
    op_kwargs={'table_name': 'silver_camaras_seguridad', 'csv_filename': 'camaras_seguridad.csv'},
    dag=dag
)

load_incidentes = PythonOperator(
    task_id='load_incidentes_trafico',
    python_callable=cargar_csv_a_postgres,
    op_kwargs={'table_name': 'silver_incidentes_trafico', 'csv_filename': 'incidentes_trafico.csv'},
    dag=dag
)

load_vehiculos = PythonOperator(
    task_id='load_vehiculos_detectados',
    python_callable=cargar_csv_a_postgres,
    op_kwargs={'table_name': 'silver_vehiculos', 'csv_filename': 'vehiculos.csv'},
    dag=dag
)

# Tareas de análisis (Transformación SQL pura - Equivalente a BigQueryInsertJobOperator)
create_golden = PostgresOperator(
    task_id='create_golden_analysis',
    postgres_conn_id='postgres_default',
    sql="""
        DROP TABLE IF EXISTS golden_analisis_trafico;
        CREATE TABLE golden_analisis_trafico AS
        SELECT
            s.sensor_id,
            s.ubicacion,
            s.velocidad_promedio,
            s.vehiculos_por_hora,
            s.ocupacion_porcentaje,
            i.tipo_incidente,
            i.severidad,
            NOW() as analyzed_at
        FROM silver_sensores_trafico s
        LEFT JOIN silver_incidentes_trafico i ON s.ubicacion = i.ubicacion;
    """,
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
