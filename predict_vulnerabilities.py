"""
Script de inferencia para detectar vulnerabilidades en código C/C++
Parte del pipeline CI/CD - Laboratorio SEMMA Software Seguro
"""

import joblib
import pandas as pd
import re
import sys
import os
from pathlib import Path

# Funciones peligrosas a detectar
DANGEROUS_FUNCTIONS = [
    'strcpy', 'gets', 'sprintf', 'strcat', 'scanf', 
    'system', 'exec', 'popen', 'memset', 'memcpy'
]

def extract_features(code):
    """
    Extrae características del código fuente para el modelo.
    Replica la misma ingeniería de features del notebook.
    """
    features = {}
    
    # Features básicas
    features['longitud'] = len(code)
    features['lineas'] = code.count('\n') + 1
    features['func_peligrosas'] = sum(code.count(func) for func in DANGEROUS_FUNCTIONS)
    
    # Detección de funciones específicas
    features['usa_strcpy'] = int('strcpy' in code)
    features['usa_gets'] = int('gets' in code)
    features['usa_system'] = int('system' in code)
    
    # Análisis de seguridad
    security_patterns = ['sanitize', 'escape', 'check', 'validate', 'safe_str']
    features['sanitizacion'] = int(any(pattern in code.lower() for pattern in security_patterns))
    
    # Complejidad ciclomática (aproximada)
    complexity_keywords = r'\b(if|while|for|case|catch|&&|\|\|)\b'
    features['complejidad_ciclomatica'] = len(re.findall(complexity_keywords, code))
    
    # Anidamiento
    features['anidamiento'] = abs(code.count('{') - code.count('}'))
    
    return pd.Series(features)


def predict_vulnerability(code_snippet, model_path='xgboost_vulnerabilidades.pkl', 
                         vectorizer_path='tfidf_vectorizer.pkl'):
    """
    Predice si un fragmento de código contiene vulnerabilidades.
    
    Args:
        code_snippet: String con el código fuente
        model_path: Ruta al modelo entrenado
        vectorizer_path: Ruta al vectorizador TF-IDF
        
    Returns:
        tuple: (predicción, probabilidad)
    """
    # Verificar que existan los modelos
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizador no encontrado: {vectorizer_path}")
    
    # Cargar modelos
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    # Extraer features manuales
    manual_features = extract_features(code_snippet).to_frame().T
    
    # Extraer features TF-IDF
    tfidf_matrix = vectorizer.transform([code_snippet])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), 
        columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    )
    
    # Combinar features
    X = pd.concat([manual_features.reset_index(drop=True), tfidf_df], axis=1)
    
    # Predicción
    probability = model.predict_proba(X)[0][1]  # Probabilidad de ser vulnerable
    prediction = "VULNERABLE" if probability > 0.7 else "SEGURO"
    
    return prediction, probability


def analyze_file(file_path, threshold=0.7):
    """
    Analiza un archivo de código fuente.
    
    Args:
        file_path: Ruta al archivo
        threshold: Umbral de probabilidad para considerar vulnerable
        
    Returns:
        dict: Resultados del análisis
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    prediction, probability = predict_vulnerability(code)
    
    return {
        'file': file_path,
        'prediction': prediction,
        'probability': probability,
        'is_vulnerable': probability > threshold
    }


def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print("Uso: python predict_vulnerabilities.py <archivo.c|archivo.cpp>")
        print("     python predict_vulnerabilities.py <directorio>")
        sys.exit(1)
    
    target = sys.argv[1]
    threshold = 0.7
    
    # Determinar si es archivo o directorio
    path = Path(target)
    
    if path.is_file():
        files_to_analyze = [path]
    elif path.is_dir():
        # Buscar archivos C/C++
        files_to_analyze = list(path.rglob('*.c')) + list(path.rglob('*.cpp'))
    else:
        print(f"Error: '{target}' no existe")
        sys.exit(1)
    
    if not files_to_analyze:
        print("No se encontraron archivos C/C++ para analizar")
        sys.exit(0)
    
    print("\n" + "="*70)
    print("  ANÁLISIS DE VULNERABILIDADES - PIPELINE CI/CD")
    print("  Modelo: XGBoost | Metodología: SEMMA")
    print("="*70 + "\n")
    
    vulnerable_files = []
    
    for file_path in files_to_analyze:
        try:
            result = analyze_file(str(file_path), threshold)
            
            status_symbol = "🚨" if result['is_vulnerable'] else "✅"
            print(f"{status_symbol} {result['file']}")
            print(f"   Predicción: {result['prediction']}")
            print(f"   Probabilidad: {result['probability']*100:.2f}%")
            print()
            
            if result['is_vulnerable']:
                vulnerable_files.append(result)
                
        except Exception as e:
            print(f"❌ Error analizando {file_path}: {e}")
            print()
    
    # Resumen
    print("="*70)
    print(f"RESUMEN: {len(vulnerable_files)}/{len(files_to_analyze)} archivos vulnerables")
    print("="*70 + "\n")
    
    if vulnerable_files:
        print("⚠️  ALERTA: Se detectaron vulnerabilidades!")
        print("\nArchivos afectados:")
        for vf in vulnerable_files:
            print(f"  - {vf['file']} ({vf['probability']*100:.1f}%)")
        sys.exit(1)  # Exit code 1 para fallar el pipeline
    else:
        print("✅ Todos los archivos pasaron la verificación de seguridad")
        sys.exit(0)


if __name__ == "__main__":
    main()
