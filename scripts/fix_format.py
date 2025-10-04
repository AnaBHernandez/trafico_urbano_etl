#!/usr/bin/env python3
"""
Script para corregir automáticamente errores de formato Python
"""
import os
import re


def fix_trailing_whitespace(file_path):
    """Eliminar espacios al final de línea"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Eliminar espacios al final de cada línea
        cleaned_lines = [line.rstrip() + '\n' for line in lines]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        return True
    except Exception as e:
        print(f"Error limpiando espacios en {file_path}: {e}")
        return False


def fix_blank_lines(file_path):
    """Arreglar líneas en blanco según PEP8"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            # Si es una función o clase, asegurar 2 líneas antes
            if re.match(r'^(def|class)\s+', line.strip()):
                # Contar líneas en blanco antes
                blank_count = 0
                j = len(new_lines) - 2
                while j >= 0 and new_lines[j].strip() == '':
                    blank_count += 1
                    j -= 1
                # Si no hay suficientes líneas en blanco, agregar
                if blank_count < 2 and len(new_lines) > 2:
                    new_lines.insert(-1, '')
                    if blank_count == 0:
                        new_lines.insert(-2, '')
            i += 1
        # Asegurar nueva línea al final
        while new_lines and new_lines[-1].strip() == '':
            new_lines.pop()
        new_lines.append('')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True
    except Exception as e:
        print(f"Error arreglando líneas en blanco en {file_path}: {e}")
        return False


def main():
    """Función principal"""
    print("🔧 CORRIGIENDO FORMATO DE ARCHIVOS PYTHON...")
    # Archivos a corregir
    files_to_fix = [
        'scripts/query_examples.py',
        'dags/trafico_urbano/trafico_diario_urbano.py',
        'dags/trafico_urbano/trafico_historico_urbano.py',
        'dags/trafico_urbano/trafico_principal.py'
    ]
    success_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"📝 Procesando: {file_path}")
            if fix_trailing_whitespace(file_path) and fix_blank_lines(file_path):
                success_count += 1
                print(f"✅ {file_path} - CORREGIDO")
            else:
                print(f"❌ {file_path} - ERROR")
        else:
            print(f"⚠️ {file_path} - NO ENCONTRADO")
    print(f"\n🎯 RESULTADO: {success_count}/{len(files_to_fix)} archivos corregidos")
    if success_count == len(files_to_fix):
        print("✅ ¡TODOS LOS ARCHIVOS CORREGIDOS!")
        return 0
    else:
        print("❌ Algunos errores persisten")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
