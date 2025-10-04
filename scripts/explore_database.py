#!/usr/bin/env python3
"""
Script para explorar la base de datos SQLite
Muestra información sobre tablas, registros y estructura
"""
import sqlite3


def explore_database():
    """Explorar la base de datos SQLite"""
    db_path = "data/trafico_urbano.db"
    print("🗄️ EXPLORANDO BASE DE DATOS SQLITE")
    print("=" * 50)
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Mostrar información general
        print("📊 INFORMACIÓN GENERAL:")
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        print(f"  📋 Total de tablas: {table_count}")
        # Listar todas las tablas
        print("\n📋 TABLAS DISPONIBLES:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📁 {table_name}: {count} registros")
        # Explorar estructura de tablas principales
        print("\n🔍 ESTRUCTURA DE TABLAS PRINCIPALES:")
        main_tables = [
            'silver_sensores_trafico',
            'silver_vehiculos_detectados',
            'golden_analisis_trafico'
        ]
        for table_name in main_tables:
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"\n  📊 {table_name}:")
                for col in columns:
                    print(f"    - {col[1]} ({col[2]})")
            except sqlite3.OperationalError:
                print(f"  ⚠️ Tabla {table_name} no encontrada")
        # Mostrar datos de ejemplo
        print("\n📄 DATOS DE EJEMPLO:")
        try:
            cursor.execute("SELECT * FROM golden_analisis_trafico LIMIT 3")
            rows = cursor.fetchall()
            if rows:
                print("  📊 golden_analisis_trafico (primeros 3 registros):")
                for row in rows:
                    print(f"    {row}")
            else:
                print("  📊 No hay datos en golden_analisis_trafico")
        except sqlite3.OperationalError:
            print("  ⚠️ No se pudo acceder a golden_analisis_trafico")
        conn.close()
        print("\n✅ Exploración completada")
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")


def get_database_stats():
    """Obtener estadísticas de la base de datos"""
    db_path = "data/trafico_urbano.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        stats = {}
        # Obtener información de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            stats[table_name] = count
        conn.close()
        return stats
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        return {}


def main():
    """Función principal"""
    print("🔍 EXPLORADOR DE BASE DE DATOS")
    print("=" * 50)
    # Explorar base de datos
    explore_database()
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS:")
    stats = get_database_stats()
    for table, count in stats.items():
        print(f"  📁 {table}: {count} registros")


if __name__ == "__main__":
    main()
