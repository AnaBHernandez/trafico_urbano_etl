from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'ana.hernandez',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definición del DAG
with DAG(
    'trafico_urbano_etl',
    default_args=default_args,
    description='Pipeline ETL para tráfico urbano (Medallion Architecture)',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['trafico', 'medallion', 'produccion'],
    catchup=False
) as dag:

    def ingesta_bronze():
        """Simula la ingesta de datos crudos"""
        logging.info("Iniciando ingesta Bronze: Sensores, Cámaras, Incidentes")
        # Aquí iría el código para leer CSVs o APIs

    def procesamiento_silver():
        """Limpieza y estandarización"""
        logging.info("Procesando capa Silver: Limpieza de nulos y tipos de datos")

    def crear_analisis_golden():
        """Genera la capa Golden agregada (Lógica de Negocio)"""
        logging.info("Generando capa Golden: Agregación por ubicación")
        # Lógica SQL representativa del portfolio
        query = """
        CREATE TABLE IF NOT EXISTS golden_analisis_trafico AS
        SELECT 
            s.ubicacion, 
            AVG(s.velocidad_promedio) as velocidad,
            COUNT(i.id) as incidentes
        FROM silver_sensores s
        LEFT JOIN silver_incidentes i ON s.ubicacion = i.ubicacion
        GROUP BY s.ubicacion
        """
        logging.info(f"Ejecutando query en base de datos: {query}")

    # Definición de Tareas
    t1_bronze = PythonOperator(
        task_id='ingesta_bronze',
        python_callable=ingesta_bronze,
    )

    t2_silver = PythonOperator(
        task_id='procesamiento_silver',
        python_callable=procesamiento_silver,
    )

    t3_golden = PythonOperator(
        task_id='crear_analisis_golden',
        python_callable=crear_analisis_golden,
    )

    # Flujo de Dependencias
    t1_bronze >> t2_silver >> t3_golden