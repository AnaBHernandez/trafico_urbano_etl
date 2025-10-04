#!/usr/bin/env python3
"""Ejemplos de consultas útiles para la base de datos"""

import sqlite3


def ejecutar_consulta(query, descripcion):
    """Ejecutar consulta y mostrar resultados"""
    print(f"\n📊 {descripcion}")
    print("-" * 50)
    try:
        conn = sqlite3.connect("data/trafico_urbano.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row}")

        conn.close()
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


if __name__ == "__main__":
    print("🔍 CONSULTAS ÚTILES PARA LA BASE DE DATOS")
    print("=" * 60)

    # Consultas útiles
    consultas = [
        ("SELECT COUNT(*) as total_sensores FROM golden_analisis_trafico", "Total de sensores"),
        ("SELECT ubicacion, velocidad_promedio FROM golden_analisis_trafico "
         "ORDER BY velocidad_promedio DESC LIMIT 5", "Top 5 velocidades más altas"),
        ("SELECT ubicacion, ocupacion_porcentaje FROM golden_analisis_trafico "
         "WHERE ocupacion_porcentaje > 80 ORDER BY ocupacion_porcentaje DESC",
         "Sensores con congestión alta"),
        ("SELECT AVG(velocidad_promedio) as velocidad_promedio, "
         "AVG(ocupacion_porcentaje) as ocupacion_promedio FROM golden_analisis_trafico",
         "Métricas promedio"),
        ("SELECT ubicacion, COUNT(*) as registros FROM golden_analisis_trafico "
         "GROUP BY ubicacion ORDER BY registros DESC LIMIT 10",
         "Top 10 ubicaciones con más datos")
    ]

    for query, descripcion in consultas:
        ejecutar_consulta(query, descripcion)
    print("\n✅ Consultas completadas")
