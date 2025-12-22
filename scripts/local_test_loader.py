"""
Script de prueba local para ejecutar las llamadas de carga sin necesidad de Airflow.
Crea archivos de ejemplo si no existen y escribe en la DB local configurada por ENV.

Uso:
  python3 scripts/local_test_loader.py
Opciones (variables de entorno):
  BRONZE_PATH (default: ./buckets/bronze-bucket/raw_data)
  DB_PATH (default: ./buckets/golden-bucket/database/trafico_urbano.db)

Este script requiere `pandas` instalado (ver `requirements.txt`).
"""
import os
from pathlib import Path
import sqlite3
import sys

try:
    import pandas as pd
except Exception:
    print("ERROR: pandas no está instalado. Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

BRONZE = Path(os.environ.get('BRONZE_PATH', Path.cwd() / 'buckets' / 'bronze-bucket' / 'raw_data'))
DB_PATH = Path(os.environ.get('DB_PATH', Path.cwd() / 'buckets' / 'golden-bucket' / 'database' / 'trafico_urbano.db'))

# Asegurar directorios
BRONZE.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Rutas de ejemplo
sensores_csv = BRONZE / 'sensores_trafico.csv'
semaforos_csv = BRONZE / 'semaforos.csv'
incidentes_csv = BRONZE / 'incidentes_trafico.csv'
camaras_csv = BRONZE / 'camaras_seguridad.csv'
vehiculos_csv = BRONZE / 'vehiculos.csv'

# Crear muestras simples si no existen
if not sensores_csv.exists():
    df = pd.DataFrame({
        'sensor_id': [1, 2],
        'ubicacion': ['A', 'B'],
        'velocidad_promedio': [30.5, 45.2],
        'vehiculos_por_hora': [120, 200],
        'ocupacion_porcentaje': [12.5, 20.0]
    })
    df.to_csv(sensores_csv, index=False)
    print(f"Creado ejemplo: {sensores_csv}")

if not semaforos_csv.exists():
    pd.DataFrame({'semaforo_id':[1], 'ubicacion':['A'], 'estado':['verde']}).to_csv(semaforos_csv, index=False)
    print(f"Creado ejemplo: {semaforos_csv}")

if not incidentes_csv.exists():
    pd.DataFrame({'id':[1], 'ubicacion':['B'], 'tipo_incidente':['choque'], 'severidad':[2]}).to_csv(incidentes_csv, index=False)
    print(f"Creado ejemplo: {incidentes_csv}")

if not camaras_csv.exists():
    pd.DataFrame({'camara_id':[1], 'ubicacion':['A'], 'status':['ok']}).to_csv(camaras_csv, index=False)
    print(f"Creado ejemplo: {camaras_csv}")

if not vehiculos_csv.exists():
    pd.DataFrame({'vehiculo_id':[1,2], 'ubicacion':['A','B']}).to_csv(vehiculos_csv, index=False)
    print(f"Creado ejemplo: {vehiculos_csv}")

# Función que carga uno por uno (simula las tareas del DAG)
def load_csv_to_table(csv_path: Path, table_name: str):
    print(f"Leyendo {csv_path} -> tabla {table_name}")
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(str(DB_PATH))
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Escrito {len(df)} filas en {table_name}")


def crear_analisis():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    try:
        cur.execute('DROP TABLE IF EXISTS golden_analisis_trafico')
        cur.execute('''
            CREATE TABLE golden_analisis_trafico AS
            SELECT s.sensor_id, s.ubicacion, s.velocidad_promedio, s.vehiculos_por_hora, s.ocupacion_porcentaje,
                   i.tipo_incidente, i.severidad
            FROM silver_sensores_trafico s
            LEFT JOIN silver_incidentes_trafico i ON s.ubicacion = i.ubicacion
        ''')
        conn.commit()
        cur.execute('SELECT COUNT(*) FROM golden_analisis_trafico')
        c = cur.fetchone()[0]
        print(f"Análisis Golden creado con {c} registros")
    except Exception as e:
        print("Error creando análisis:", e)
    finally:
        conn.close()


if __name__ == '__main__':
    load_csv_to_table(sensores_csv, 'silver_sensores_trafico')
    load_csv_to_table(semaforos_csv, 'silver_semaforos')
    load_csv_to_table(incidentes_csv, 'silver_incidentes_trafico')
    load_csv_to_table(camaras_csv, 'silver_camaras_seguridad')
    load_csv_to_table(vehiculos_csv, 'silver_vehiculos')
    crear_analisis()
    print('Prueba local completada.')
