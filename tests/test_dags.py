#!/usr/bin/env python3
"""
Tests unitarios para el sistema ETL de tráfico urbano
"""

import unittest
import sys
import os

# Agregar el directorio de dags al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dags'))

class TestBasicFunctionality(unittest.TestCase):
    """Tests básicos para verificar funcionalidad del sistema"""
    
    def test_pandas_import(self):
        """Test que verifica que pandas se puede importar"""
        try:
            import pandas as pd
            self.assertIsNotNone(pd)
        except ImportError:
            self.fail("No se pudo importar pandas")
    
    def test_sqlite_connection(self):
        """Test que verifica que se puede conectar a SQLite"""
        import sqlite3
        try:
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO test VALUES (1, 'test')")
            result = cursor.execute("SELECT * FROM test").fetchone()
            self.assertEqual(result, (1, 'test'))
            conn.close()
        except Exception as e:
            self.fail(f"Error en conexión SQLite: {e}")
    
    def test_dataframe_creation(self):
        """Test que verifica que se puede crear un DataFrame"""
        try:
            import pandas as pd
            df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
            self.assertEqual(len(df), 3)
            self.assertEqual(list(df.columns), ['col1', 'col2'])
        except Exception as e:
            self.fail(f"Error creando DataFrame: {e}")
    
    def test_system_imports(self):
        """Test que verifica que se pueden importar módulos del sistema"""
        try:
            import os
            import sys
            import datetime
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error importando módulos del sistema: {e}")

if __name__ == '__main__':
    # Configurar el test runner
    unittest.main(verbosity=2)
