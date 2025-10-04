#!/usr/bin/env python3
"""
Script para ejecutar tests del sistema ETL
"""

import sys
# import os  # No utilizado
import subprocess


def run_tests():
    """Ejecutar tests unitarios"""
    print("🧪 Ejecutando tests unitarios...")

    try:
        # Ejecutar pytest
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/',
            '-v',
            '--tb=short',
            '--cov=dags',
            '--cov-report=term-missing'
        ], capture_output=True, text=True)

        print("📊 Resultado de tests:")
        print(result.stdout)

        if result.stderr:
            print("⚠️ Errores:")
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")
        return False


def run_linting():
    """Ejecutar linting del código"""
    print("🔍 Ejecutando linting...")

    try:
        # Ejecutar flake8
        result = subprocess.run([
            sys.executable, '-m', 'flake8',
            'dags/',
            'scripts/',
            '--max-line-length=100',
            '--ignore=E203,W503'
        ], capture_output=True, text=True)

        if result.stdout:
            print("📝 Linting issues:")
            print(result.stdout)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error ejecutando linting: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 Iniciando tests del sistema ETL...")

    # Ejecutar tests
    tests_ok = run_tests()

    # Ejecutar linting
    linting_ok = run_linting()

    # Resultado final
    if tests_ok and linting_ok:
        print("✅ Todos los tests pasaron correctamente")
        return 0
    else:
        print("❌ Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
