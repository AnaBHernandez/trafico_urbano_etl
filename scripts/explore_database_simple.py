#!/usr/bin/env python3
"""
Script simple para explorar la base de datos SQLite
Versión simplificada del explorador
"""
import sqlite3


def explore_database_simple():
    """Explorar la base de datos de forma simple"""
    db_path = "data/trafico_urbano.db"
    print("🗄️ EXPLORACIÓN SIMPLE DE BASE DE DATOS")
    print("=" * 50)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Contar tablas
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        print(f"📋 Total de tablas: {table_count}")
        # Listar tablas
        print("\n📋 TABLAS:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📁 {table_name}: {count} registros")
        conn.close()
        print("\n✅ Exploración completada")
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    explore_database_simple()
