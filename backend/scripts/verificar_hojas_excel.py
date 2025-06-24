import pandas as pd
import sys
import os

def verificar_hojas_excel(archivo_path):
    """
    Verifica las hojas disponibles en un archivo Excel
    """
    try:
        # Leer todas las hojas del archivo
        excel_file = pd.ExcelFile(archivo_path)
        
        print(f"📊 Archivo: {archivo_path}")
        print(f"📋 Hojas encontradas ({len(excel_file.sheet_names)}):")
        print("-" * 50)
        
        for i, nombre_hoja in enumerate(excel_file.sheet_names, 1):
            print(f"{i}. '{nombre_hoja}'")
            
            # Mostrar información básica de cada hoja
            try:
                df = pd.read_excel(archivo_path, sheet_name=nombre_hoja)
                print(f"   - Filas: {len(df)}")
                print(f"   - Columnas: {len(df.columns)}")
                print(f"   - Columnas: {list(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            except Exception as e:
                print(f"   - Error al leer: {e}")
            print()
        
        # Buscar hojas que podrían ser de inteligencias
        print("🔍 Buscando hojas que podrían contener datos de inteligencias:")
        print("-" * 50)
        
        palabras_clave = ['inteligencia', 'inteligencias', 'intel', 'multiple', 'múltiple', 'brain', 'cerebro']
        
        for nombre_hoja in excel_file.sheet_names:
            nombre_lower = nombre_hoja.lower()
            for palabra in palabras_clave:
                if palabra in nombre_lower:
                    print(f"✅ Posible hoja de inteligencias: '{nombre_hoja}'")
                    break
        
        return excel_file.sheet_names
        
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python verificar_hojas_excel.py <ruta_del_archivo_excel>")
        print("Ejemplo: python verificar_hojas_excel.py datos.xlsx")
        sys.exit(1)
    
    archivo = sys.argv[1]
    if not os.path.exists(archivo):
        print(f"❌ El archivo '{archivo}' no existe")
        sys.exit(1)
    
    hojas = verificar_hojas_excel(archivo) 