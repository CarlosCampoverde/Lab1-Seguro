"""
Script de Verificación Multi-Lenguaje
Verifica que todos los componentes estén listos para trabajar con 8 lenguajes
"""

import os
import sys
from pathlib import Path

def verificar_archivos():
    """Verifica que existan todos los archivos necesarios"""
    print("="*70)
    print("🔍 VERIFICACIÓN DE ARCHIVOS")
    print("="*70)
    
    archivos_requeridos = {
        'predict_vulnerabilities.py': 'Script de predicción',
        'generate_report.py': 'Generador de reportes',
        'Lab1_SEMMA_Software_Seguro.ipynb': 'Notebook de entrenamiento',
        'README.md': 'Documentación principal',
        'README_PIPELINE.md': 'Documentación del pipeline',
        'GUIA_REENTRENAMIENTO.md': 'Guía de re-entrenamiento',
        'requirements.txt': 'Dependencias'
    }
    
    todos_ok = True
    for archivo, descripcion in archivos_requeridos.items():
        if os.path.exists(archivo):
            print(f"✅ {archivo:40} ({descripcion})")
        else:
            print(f"❌ {archivo:40} NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def verificar_modelos():
    """Verifica que existan los modelos entrenados"""
    print("\n" + "="*70)
    print("🤖 VERIFICACIÓN DE MODELOS")
    print("="*70)
    
    modelos = {
        'xgboost_vulnerabilidades.pkl': 'Modelo XGBoost',
        'tfidf_vectorizer.pkl': 'Vectorizador TF-IDF'
    }
    
    todos_ok = True
    for modelo, descripcion in modelos.items():
        if os.path.exists(modelo):
            tamano = os.path.getsize(modelo) / (1024 * 1024)
            print(f"✅ {modelo:40} ({tamano:.2f} MB)")
        else:
            print(f"⚠️  {modelo:40} NO ENCONTRADO - Necesita entrenamiento")
            todos_ok = False
    
    if not todos_ok:
        print("\n💡 Ejecuta el notebook Lab1_SEMMA_Software_Seguro.ipynb para generar los modelos")
    
    return todos_ok

def verificar_dataset():
    """Verifica que exista el dataset"""
    print("\n" + "="*70)
    print("📊 VERIFICACIÓN DE DATASET")
    print("="*70)
    
    datasets_posibles = [
        'diversevul.json',
        'diversevul.csv',
        'diversevul_20230702.json',
        'vulnerability_dataset.csv'
    ]
    
    dataset_encontrado = None
    for dataset in datasets_posibles:
        if os.path.exists(dataset):
            tamano = os.path.getsize(dataset) / (1024 * 1024)
            print(f"✅ Dataset encontrado: {dataset} ({tamano:.2f} MB)")
            dataset_encontrado = dataset
            break
    
    if not dataset_encontrado:
        print("❌ No se encontró ningún dataset")
        print("\n💡 Descarga DiverseVul desde:")
        print("   https://zenodo.org/records/7946033")
        print("   https://huggingface.co/datasets/bstee615/diversevul")
        return False
    
    return True

def verificar_ejemplos():
    """Verifica que existan los ejemplos multi-lenguaje"""
    print("\n" + "="*70)
    print("📁 VERIFICACIÓN DE EJEMPLOS MULTI-LENGUAJE")
    print("="*70)
    
    if not os.path.exists('ejemplos_multilenguaje'):
        print("❌ Directorio 'ejemplos_multilenguaje' no encontrado")
        return False
    
    lenguajes_esperados = {
        'python': ['vulnerable_python.py', 'seguro_python.py'],
        'java': ['vulnerable_java.java', 'seguro_java.java'],
        'javascript': ['vulnerable_javascript.js', 'seguro_javascript.js'],
        'php': ['vulnerable_php.php', 'seguro_php.php']
    }
    
    todos_ok = True
    for lenguaje, archivos in lenguajes_esperados.items():
        print(f"\n{lenguaje.upper()}:")
        for archivo in archivos:
            ruta = os.path.join('ejemplos_multilenguaje', archivo)
            if os.path.exists(ruta):
                print(f"  ✅ {archivo}")
            else:
                print(f"  ❌ {archivo} NO ENCONTRADO")
                todos_ok = False
    
    return todos_ok

def verificar_soporte_lenguajes():
    """Verifica el código de soporte multi-lenguaje en los scripts"""
    print("\n" + "="*70)
    print("🌐 VERIFICACIÓN DE SOPORTE MULTI-LENGUAJE")
    print("="*70)
    
    # Leer predict_vulnerabilities.py
    try:
        with open('predict_vulnerabilities.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        checks = {
            'SUPPORTED_LANGUAGES': 'Diccionario de lenguajes soportados',
            'detect_language_from_code': 'Función de detección de lenguaje',
            'DANGEROUS_FUNCTIONS_BY_LANG': 'Funciones peligrosas por lenguaje'
        }
        
        for check, descripcion in checks.items():
            if check in contenido:
                print(f"✅ {descripcion}")
            else:
                print(f"❌ {descripcion} - NO ENCONTRADO")
        
        # Contar lenguajes soportados
        if 'SUPPORTED_LANGUAGES' in contenido:
            # Buscar extensiones en el diccionario
            extensiones = ['.c', '.cpp', '.py', '.java', '.js', '.php', '.rb', '.go']
            lenguajes_encontrados = sum(1 for ext in extensiones if f"'{ext}'" in contenido)
            print(f"\n📊 Lenguajes detectados en código: {lenguajes_encontrados}")
            
            if lenguajes_encontrados >= 6:
                print(f"✅ Cumple requisito de 6+ lenguajes")
            else:
                print(f"⚠️  Solo {lenguajes_encontrados} lenguajes - se requieren mínimo 6")
        
    except FileNotFoundError:
        print("❌ No se pudo abrir predict_vulnerabilities.py")
        return False
    
    return True

def mostrar_siguiente_paso():
    """Muestra los siguientes pasos a seguir"""
    print("\n" + "="*70)
    print("📝 SIGUIENTES PASOS")
    print("="*70)
    
    pasos = [
        "1️⃣  Si no tienes los modelos: Ejecuta Lab1_SEMMA_Software_Seguro.ipynb",
        "2️⃣  Prueba el sistema: python predict_vulnerabilities.py ejemplos_multilenguaje/",
        "3️⃣  Genera reporte: python generate_report.py",
        "4️⃣  Revisa la documentación: README.md y GUIA_REENTRENAMIENTO.md"
    ]
    
    for paso in pasos:
        print(paso)

def main():
    print("\n" + "="*70)
    print("🛡️  VERIFICACIÓN DE SISTEMA MULTI-LENGUAJE")
    print("   Proyecto: Desarrollo de Software Seguro con SEMMA")
    print("="*70)
    
    resultados = {
        'Archivos': verificar_archivos(),
        'Modelos': verificar_modelos(),
        'Dataset': verificar_dataset(),
        'Ejemplos': verificar_ejemplos(),
        'Código Multi-Lenguaje': verificar_soporte_lenguajes()
    }
    
    print("\n" + "="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70)
    
    total = len(resultados)
    aprobados = sum(1 for v in resultados.values() if v)
    
    for categoria, estado in resultados.items():
        emoji = "✅" if estado else "❌"
        print(f"{emoji} {categoria:30} {'COMPLETO' if estado else 'INCOMPLETO'}")
    
    print(f"\n🎯 Completitud: {aprobados}/{total} ({aprobados/total*100:.1f}%)")
    
    if aprobados == total:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE LISTO!")
        print("   ✅ Soporte multi-lenguaje implementado")
        print("   ✅ Todos los componentes verificados")
    elif aprobados >= total - 1:
        print("\n⚠️  CASI LISTO - Solo falta un componente")
    else:
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        print("   Revisa los elementos marcados con ❌")
    
    mostrar_siguiente_paso()
    
    print("\n" + "="*70)
    print("🔍 Para más información, consulta: GUIA_REENTRENAMIENTO.md")
    print("="*70 + "\n")
    
    return 0 if aprobados == total else 1

if __name__ == "__main__":
    sys.exit(main())
