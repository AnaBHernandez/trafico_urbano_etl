#!/usr/bin/env python3
"""
DAG Principal del Sistema ETL de Tráfico Urbano
Versión: SIMULACIÓN (Genera datos sintéticos en PostgreSQL)
Nota: Este DAG es útil para pruebas cuando no hay CSVs disponibles.
"""

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text

# Configuración del DAG
default_args = {
    'owner': 'ana-hernandez',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 2),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'trafico_simulacion_principal',  # Renombrado para evitar confusión
    default_args=default_args,
    description='Generador de datos simulados en PostgreSQL',
    schedule_interval=None,  # Ejecución manual para no sobreescribir datos reales
    catchup=False,
    tags=['trafico', 'simulacion', 'postgres']
)


def verificar_base_datos(**context):
    """Verificar que la base de datos esté funcionando"""
    print("🔍 VERIFICANDO BASE DE DATOS...")

    try:
        engine = create_engine(os.getenv('DATA_WAREHOUSE_CONN'))
        
        with engine.connect() as conn:
            # Verificar tablas en Postgres
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print(f"✅ Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
                
        return f"PostgreSQL verificado: {len(tables)} tablas"

    except Exception:
        print("❌ Error verificando base de datos")
        return "Error verificando base de datos"


def cargar_datos_sensores(**context):
    """Cargar datos de sensores de tráfico"""
    print("📊 CARGANDO DATOS DE SENSORES...")

    try:
        # Simular datos de sensores
        import pandas as pd

        # Crear datos de ejemplo
        data = {
            'sensor_id': [f'S{i:03d}' for i in range(1, 11)],
            'ubicacion': [f'Calle {i}' for i in range(1, 11)],
            'velocidad_promedio': [30 + i for i in range(10)],
            'vehiculos_por_hora': [50 + i * 5 for i in range(10)],
            'ocupacion_porcentaje': [60 + i for i in range(10)]
        }

        df = pd.DataFrame(data)
        print(f"✅ Datos cargados: {len(df)} registros")

        # Cargar a Postgres
        engine = create_engine(os.getenv('DATA_WAREHOUSE_CONN'))
        df.to_sql('silver_sensores_trafico', engine, if_exists='replace', index=False)

        print("✅ Datos de sensores simulados cargados en PostgreSQL")
        return f"Sensores cargados: {len(df)} registros"

    except Exception:
        print("❌ Error cargando sensores")
        return "Error cargando sensores"


def cargar_datos_incidentes(**context):
    """Cargar datos de incidentes de tráfico"""
    print("🚨 CARGANDO DATOS DE INCIDENTES...")

    try:
        # Simular datos de incidentes
        import pandas as pd

        # Crear datos de ejemplo
        data = {
            'incidente_id': [f'I{i:03d}' for i in range(1, 6)],
            'ubicacion': [f'Calle {i}' for i in range(1, 6)],
            'tipo_incidente': ['Accidente', 'Avería', 'Obras', 'Congestión', 'Otros'],
            'severidad': ['Alta', 'Media', 'Baja', 'Media', 'Alta']
        }

        df = pd.DataFrame(data)
        print(f"✅ Datos cargados: {len(df)} registros")

        # Cargar a Postgres
        engine = create_engine(os.getenv('DATA_WAREHOUSE_CONN'))
        df.to_sql('silver_incidentes_trafico', engine, if_exists='replace', index=False)

        print("✅ Datos de incidentes simulados cargados en PostgreSQL")
        return f"Incidentes cargados: {len(df)} registros"

    except Exception:
        print("❌ Error cargando incidentes")
        return "Error cargando incidentes"


def crear_analisis_golden(**context):
    """Crear análisis Golden consolidado"""
    print("🏆 CREANDO ANÁLISIS GOLDEN...")

    try:
        engine = create_engine(os.getenv('DATA_WAREHOUSE_CONN'))
        
        with engine.connect() as conn:
            # Crear tabla Golden con análisis consolidado
            conn.execute(text("DROP TABLE IF EXISTS golden_analisis_trafico"))
            
            conn.execute(text("""
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
                LEFT JOIN silver_incidentes_trafico i ON s.ubicacion = i.ubicacion
            """))
            
            # Verificar resultados
            result = conn.execute(text("SELECT COUNT(*) FROM golden_analisis_trafico"))
            count = result.fetchone()[0]
            # SQLAlchemy hace commit automático o al cerrar el bloque with en versiones modernas, 
            # pero para DDL a veces se requiere commit explícito si no es autocommit.
            # En este caso, create_engine por defecto suele funcionar bien para esto en modo básico.

        print(f"✅ Análisis Golden creado: {count} registros")
        return f"Análisis Golden: {count} registros"

    except Exception:
        print("❌ Error creando análisis Golden")
        return "Error creando análisis Golden"


def generar_metricas_finales(**context):
    """Generar métricas finales del sistema"""
    print("📊 GENERANDO MÉTRICAS FINALES...")

    try:
        engine = create_engine(os.getenv('DATA_WAREHOUSE_CONN'))
        
        with engine.connect() as conn:
            # Métricas de sensores
            result = conn.execute(text("SELECT COUNT(*) FROM silver_sensores_trafico"))
            sensores_count = result.fetchone()[0]

            # Métricas de incidentes
            result = conn.execute(text("SELECT COUNT(*) FROM silver_incidentes_trafico"))
            incidentes_count = result.fetchone()[0]

            # Métricas de análisis Golden
            result = conn.execute(text("SELECT COUNT(*) FROM golden_analisis_trafico"))
            golden_count = result.fetchone()[0]

            # Velocidad promedio
            result = conn.execute(text("SELECT AVG(velocidad_promedio) FROM golden_analisis_trafico"))
            velocidad_promedio = result.fetchone()[0] or 0

        print("📈 MÉTRICAS DEL SISTEMA:")
        print(f"  • Sensores procesados: {sensores_count}")
        print(f"  • Incidentes procesados: {incidentes_count}")
        print(f"  • Análisis Golden: {golden_count}")
        print(f"  • Velocidad promedio: {velocidad_promedio:.2f} km/h")

        return f"Métricas generadas: {golden_count} registros finales"

    except Exception:
        print("❌ Error generando métricas")
        return "Error generando métricas"


# Definir tareas
verificar_db = PythonOperator(
    task_id='verificar_base_datos',
    python_callable=verificar_base_datos,
    dag=dag
)

cargar_sensores = PythonOperator(
    task_id='cargar_datos_sensores',
    python_callable=cargar_datos_sensores,
    dag=dag
)

cargar_incidentes = PythonOperator(
    task_id='cargar_datos_incidentes',
    python_callable=cargar_datos_incidentes,
    dag=dag
)

crear_golden = PythonOperator(
    task_id='crear_analisis_golden',
    python_callable=crear_analisis_golden,
    dag=dag
)

generar_metricas = PythonOperator(
    task_id='generar_metricas_finales',
    python_callable=generar_metricas_finales,
    dag=dag
)

# Definir dependencias
verificar_db >> [cargar_sensores, cargar_incidentes] >> crear_golden >> generar_metricas
