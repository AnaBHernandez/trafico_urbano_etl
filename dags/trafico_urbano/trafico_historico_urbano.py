# DAG HISTÓRICO - Análisis de Tráfico Urbano - COMPLETAMENTE OPTIMIZADO
# Fecha: 24 Septiembre 2025
# Propósito: Análisis histórico de tráfico urbano - MÁXIMO 10 MINUTOS
# Estado: MANUAL (desarrollo/formación)
# OPTIMIZACIÓN: Análisis de datos históricos

import pendulum
from airflow.models.dag import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

# =====================================================
# VARIABLES DE CONFIGURACIÓN
# =====================================================
DB_PATH = '/opt/airflow/buckets/golden-bucket/database/trafico_urbano.db'
DAG_ID = 'trafico_historico_urbano'

# =====================================================
# FUNCIONES PYTHON PARA REEMPLAZAR SQLiteOperator
# =====================================================


def analizar_congestiones_historicas(**context):
    """Analiza congestiones históricas por ubicación"""
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ubicacion,
            COUNT(*) as total_congestiones,
            AVG(ocupacion_porcentaje) as ocupacion_promedio,
            MAX(ocupacion_porcentaje) as ocupacion_maxima
        FROM golden_analisis_trafico
        WHERE ocupacion_porcentaje > 80
        AND DATE(analyzed_at) >= DATE('now', '-30 days')
        GROUP BY ubicacion
        ORDER BY total_congestiones DESC
        LIMIT 10
    """)

    resultados = cursor.fetchall()

    print("📊 ANÁLISIS DE CONGESTIONES HISTÓRICAS:")
    for ubicacion, total, promedio, maxima in resultados:
        print(
            f"  • {ubicacion}: {total} congestiones, "
            f"{promedio:.1f}% promedio, {maxima:.1f}% máxima"
        )

    conn.close()
    return f"Congestiones analizadas: {len(resultados)} ubicaciones"


def analizar_tendencias_historicas(**context):
    """Analiza tendencias históricas de tráfico"""
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            strftime('%H', analyzed_at) as hora,
            AVG(velocidad_promedio) as velocidad_promedio,
            AVG(vehiculos_por_hora) as vehiculos_promedio,
            AVG(ocupacion_porcentaje) as ocupacion_promedio
        FROM golden_analisis_trafico
        WHERE DATE(analyzed_at) >= DATE('now', '-30 days')
        GROUP BY strftime('%H', analyzed_at)
        ORDER BY hora
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print("📈 TENDENCIAS HISTÓRICAS DE TRÁFICO:")
    print("  - Período analizado: Últimos 30 días")
    print(f"  - Registros procesados: {len(df)}")

    if len(df) > 0:
        print("  - Patrones identificados:")
        print(f"    • Hora pico: {df.loc[df['vehiculos_promedio'].idxmax(), 'hora']}:00")
        print(f"    • Velocidad promedio: {df['velocidad_promedio'].mean():.1f} km/h")
        print(f"    • Ocupación promedio: {df['ocupacion_promedio'].mean():.1f}%")

    return f"Tendencias analizadas: {len(df)} períodos"


def metricas_rendimiento_historico(**context):
    """Genera métricas de rendimiento histórico"""
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Métricas generales
    cursor.execute("SELECT COUNT(*) FROM golden_analisis_trafico")
    total_registros = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(velocidad_promedio) FROM golden_analisis_trafico
        WHERE DATE(analyzed_at) >= DATE('now', '-7 days')
    """)
    velocidad_semanal = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT AVG(ocupacion_porcentaje) FROM golden_analisis_trafico
        WHERE DATE(analyzed_at) >= DATE('now', '-7 days')
    """)
    ocupacion_semanal = cursor.fetchone()[0] or 0

    conn.close()

    print("📊 MÉTRICAS DE RENDIMIENTO HISTÓRICO:")
    print(f"  - Total de registros: {total_registros}")
    print(f"  - Velocidad promedio (7 días): {velocidad_semanal:.1f} km/h")
    print(f"  - Ocupación promedio (7 días): {ocupacion_semanal:.1f}%")

    return f"Métricas generadas: {total_registros} registros históricos"


def generar_reporte_semanal(**context):
    """Genera reporte semanal consolidado"""
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            DATE(analyzed_at) as fecha,
            COUNT(*) as registros,
            AVG(velocidad_promedio) as velocidad_promedio,
            AVG(vehiculos_por_hora) as vehiculos_promedio,
            AVG(ocupacion_porcentaje) as ocupacion_promedio
        FROM golden_analisis_trafico
        WHERE DATE(analyzed_at) >= DATE('now', '-7 days')
        GROUP BY DATE(analyzed_at)
        ORDER BY fecha
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print("📈 REPORTE SEMANAL DE TRÁFICO:")
    print("  - Período: Últimos 7 días")
    print(f"  - Registros analizados: {len(df)}")

    if len(df) > 0:
        print("  - Resumen semanal:")
        print(f"    • Días con datos: {len(df)}")
        print(f"    • Velocidad promedio: {df['velocidad_promedio'].mean():.1f} km/h")
        print(f"    • Vehículos promedio: {df['vehiculos_promedio'].mean():.1f}/h")
        print(f"    • Ocupación promedio: {df['ocupacion_promedio'].mean():.1f}%")

    return f"Reporte semanal generado: {len(df)} días analizados"


# =====================================================
# CONFIGURACIÓN DEL DAG
# =====================================================
default_args = {
    'owner': 'ana-hernandez',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2025, 9, 24, tz="UTC"),
    'retries': 0,
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False
}

dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='Análisis histórico de tráfico urbano',
    schedule_interval='@weekly',
    catchup=False,
    tags=['trafico', 'historico', 'analisis']
)

# =====================================================
# TAREAS DEL DAG
# =====================================================
start = DummyOperator(
    task_id='start',
    dag=dag
)

# Tareas de análisis histórico
analyze_congestiones = PythonOperator(
    task_id='analizar_congestiones_historicas',
    python_callable=analizar_congestiones_historicas,
    dag=dag
)

analyze_tendencias = PythonOperator(
    task_id='analizar_tendencias_historicas',
    python_callable=analizar_tendencias_historicas,
    dag=dag
)

generate_metrics = PythonOperator(
    task_id='metricas_rendimiento_historico',
    python_callable=metricas_rendimiento_historico,
    dag=dag
)

generate_report = PythonOperator(
    task_id='generar_reporte_semanal',
    python_callable=generar_reporte_semanal,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

# =====================================================
# DEPENDENCIAS DEL DAG
# =====================================================
start >> [analyze_congestiones, analyze_tendencias] >> generate_metrics >> generate_report >> end
