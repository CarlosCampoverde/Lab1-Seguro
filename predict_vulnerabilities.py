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

# Mapeo de extensiones a lenguajes soportados
SUPPORTED_LANGUAGES = {
    '.c': 'C',
    '.h': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.hpp': 'C++',
    '.java': 'Java',
    '.py': 'Python',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript',
    '.ts': 'TypeScript',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.go': 'Go'
}

# Funciones peligrosas por lenguaje
DANGEROUS_FUNCTIONS = {
    'C': ['strcpy', 'gets', 'sprintf', 'strcat', 'scanf', 'system', 'exec', 'popen', 'memset', 'memcpy'],
    'C++': ['strcpy', 'gets', 'sprintf', 'strcat', 'scanf', 'system', 'exec', 'popen', 'memset', 'memcpy'],
    'Python': ['eval', 'exec', 'compile', '__import__', 'pickle.loads', 'input', 'os.system'],
    'Java': ['Runtime.exec', 'ProcessBuilder', 'ScriptEngine', 'readObject', 'Class.forName'],
    'JavaScript': ['eval', 'Function', 'innerHTML', 'document.write', 'dangerouslySetInnerHTML'],
    'TypeScript': ['eval', 'Function', 'innerHTML', 'document.write', 'dangerouslySetInnerHTML'],
    'PHP': ['eval', 'exec', 'system', 'shell_exec', 'passthru', 'unserialize', 'include', 'require'],
    'Ruby': ['eval', 'exec', 'system', 'send', 'instance_eval', 'class_eval', 'Marshal.load'],
    'Go': ['exec.Command', 'os.Exec', 'syscall.Exec', 'unsafe.Pointer']
}

def detect_language_from_code(code, file_extension=None):
    """
    Detecta el lenguaje de programación basado en patrones de código.
    """
    if file_extension and file_extension in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[file_extension]
    
    # Detección heurística
    if 'public class' in code or 'import java.' in code:
        return 'Java'
    elif 'def ' in code and 'import ' in code and ':' in code:
        return 'Python'
    elif '<?php' in code or '$_' in code:
        return 'PHP'
    elif 'function' in code and '=>' in code:
        return 'JavaScript'
    elif 'package main' in code and 'func ' in code:
        return 'Go'
    elif 'def ' in code and 'end' in code:
        return 'Ruby'
    elif '#include' in code or 'int main' in code:
        return 'C' if '.c' in str(file_extension) else 'C++'
    else:
        return 'C'  # Default para backward compatibility


def extract_features(code, language=None, file_extension=None):
    """
    Extrae características del código fuente para el modelo.
    Soporta múltiples lenguajes de programación.
    
    Args:
        code: Código fuente
        language: Lenguaje de programación (opcional)
        file_extension: Extensión del archivo (opcional)
    """
    f = {}
    code_lower = code.lower()
    
    # Funciones peligrosas (multi-lenguaje)
    dangerous_c = ['strcpy','gets','sprintf','strcat','scanf','system','exec','popen','memset','memcpy']
    dangerous_java = ['Runtime.exec','ProcessBuilder','eval','deserialize','readObject']
    dangerous_python = ['eval','exec','pickle.loads','subprocess','os.system','__import__']
    dangerous_js = ['eval','innerHTML','document.write','setTimeout','setInterval']
    
    # Features básicas (universal para todos los lenguajes)
    f['longitud'] = len(code)
    f['lineas'] = code.count('\n') + 1
    f['long_prom_linea'] = f['longitud'] / max(f['lineas'], 1)
    
    # Funciones peligrosas (multi-lenguaje)
    f['func_peligrosas_c'] = sum(code.count(w) for w in dangerous_c)
    f['func_peligrosas_java'] = sum(code.count(w) for w in dangerous_java)
    f['func_peligrosas_python'] = sum(code.count(w) for w in dangerous_python)
    f['func_peligrosas_js'] = sum(code.count(w) for w in dangerous_js)
    f['total_peligrosas'] = f['func_peligrosas_c'] + f['func_peligrosas_java'] + f['func_peligrosas_python'] + f['func_peligrosas_js']
    
    # Funciones específicas críticas
    f['usa_strcpy'] = int('strcpy' in code)
    f['usa_gets'] = int('gets' in code)
    f['usa_eval'] = int('eval' in code)
    f['usa_exec'] = int('exec' in code)
    
    # Sanitización y validación
    f['sanitizacion'] = int(any(p in code_lower for p in ['sanitize','escape','check','validate','safe','filter']))
    
    # Complejidad ciclomática (universal)
    f['complejidad_ciclomatica'] = len(re.findall(r'\b(if|while|for|case|catch|&&|\|\||switch|else)\b', code))
    
    # Anidamiento (basado en brackets)
    f['anidamiento'] = abs(code.count('{') - code.count('}'))
    
    # Características adicionales
    f['comentarios'] = code.count('//') + code.count('/*') + code.count('#')
    f['imports'] = code.count('import') + code.count('include') + code.count('require')
    f['excepciones'] = code.count('try') + code.count('catch') + code.count('except') + code.count('finally')
    
    # Detección simple de lenguaje (heurística)
    if 'def ' in code or 'import ' in code or 'print(' in code:
        f['es_python'] = 1
    else:
        f['es_python'] = 0
        
    if 'public class' in code or 'private ' in code or 'void ' in code:
        f['es_java'] = 1
    else:
        f['es_java'] = 0
        
    if 'function' in code or 'const ' in code or 'let ' in code or '=> ' in code:
        f['es_javascript'] = 1
    else:
        f['es_javascript'] = 0
    
    # FEATURES AVANZADAS DE SEGURIDAD (para mejorar accuracy)
    # Patrones de validación de entrada
    f['tiene_validacion_null'] = int('null' in code_lower or 'nullptr' in code_lower or 'none' in code_lower)
    f['tiene_validacion_length'] = int('length' in code_lower or 'size' in code_lower or 'len(' in code_lower)
    f['tiene_limites'] = int('min' in code_lower or 'max' in code_lower or 'limit' in code_lower)
    
    # Funciones seguras alternativas
    f['usa_funciones_seguras'] = int(any(w in code for w in ['strncpy', 'snprintf', 'fgets', 'strncat']))
    f['tiene_constantes_tamano'] = int('#define' in code or 'const ' in code or 'final ' in code)
    
    # Manejo de errores
    f['densidad_excepciones'] = f['excepciones'] / max(f['lineas'], 1)
    f['tiene_return_error'] = int('return -1' in code or 'return null' in code_lower or 'return false' in code_lower)
    
    # Ratio de complejidad vs tamaño
    f['ratio_complejidad'] = f['complejidad_ciclomatica'] / max(f['lineas'], 1)
    f['ratio_comentarios'] = f['comentarios'] / max(f['lineas'], 1)
    
    return pd.Series(f)


def predict_vulnerability(code_snippet, model_path='xgboost_vulnerabilidades.pkl', 
                         vectorizer_path='tfidf_vectorizer.pkl', file_extension=None):
    """
    Predice si un fragmento de código contiene vulnerabilidades.
    Soporta múltiples lenguajes de programación.
    
    Args:
        code_snippet: String con el código fuente
        model_path: Ruta al modelo entrenado
        vectorizer_path: Ruta al vectorizador TF-IDF
        file_extension: Extensión del archivo (para detectar lenguaje)
        
    Returns:
        tuple: (predicción, probabilidad, lenguaje)
    """
    # Verificar que existan los modelos
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizador no encontrado: {vectorizer_path}")
    
    # Cargar modelos
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    # Detectar lenguaje
    language = detect_language_from_code(code_snippet, file_extension)
    
    # Extraer features manuales
    manual_features = extract_features(code_snippet, language, file_extension).to_frame().T
    
    # Extraer features TF-IDF
    tfidf_matrix = vectorizer.transform([code_snippet])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), 
        columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    )
    
    # Combinar features
    X = pd.concat([manual_features.reset_index(drop=True), tfidf_df], axis=1)
    
    # Predicción
    probability = model.predict_proba(X)[0][1]  # Nivel de confianza
    prediction = "VULNERABLE" if probability > 0.7 else "SEGURO"
    
    return prediction, probability, language


def analyze_file(file_path, threshold=0.7):
    """
    Analiza un archivo de código fuente.
    Soporta múltiples lenguajes de programación.
    
    Args:
        file_path: Ruta al archivo
        threshold: Umbral de nivel de confianza para considerar vulnerable
        
    Returns:
        dict: Resultados del análisis
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    # Obtener extensión del archivo
    file_extension = Path(file_path).suffix.lower()
    
    prediction, probability, language = predict_vulnerability(code, file_extension=file_extension)
    
    return {
        'file': file_path,
        'prediction': prediction,
        'probability': probability,
        'language': language,
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
        # Buscar archivos de todos los lenguajes soportados
        files_to_analyze = []
        for ext in SUPPORTED_LANGUAGES.keys():
            files_to_analyze.extend(list(path.rglob(f'*{ext}')))
        # Ordenar por lenguaje para mejor presentación
        files_to_analyze = sorted(files_to_analyze, key=lambda x: x.suffix)
    else:
        print(f"Error: '{target}' no existe")
        sys.exit(1)
    
    if not files_to_analyze:
        supported_exts = ', '.join(SUPPORTED_LANGUAGES.keys())
        print(f"No se encontraron archivos soportados para analizar")
        print(f"Extensiones soportadas: {supported_exts}")
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
            lang_emoji = {
                'C': '🔵', 'C++': '🔷', 'Python': '🐍', 'Java': '☕',
                'JavaScript': '📜', 'TypeScript': '📘', 'PHP': '🐘',
                'Ruby': '💎', 'Go': '🔷'
            }.get(result['language'], '📄')
            
            print(f"{status_symbol} {lang_emoji} [{result['language']}] {result['file']}")
            print(f"   Predicción: {result['prediction']}")
            print(f"   Nivel de confianza: {result['probability']*100:.2f}%")
            print()
            
            if result['is_vulnerable']:
                vulnerable_files.append(result)
                
        except Exception as e:
            print(f"❌ Error analizando {file_path}: {e}")
            print()
    
    # Estadísticas por lenguaje
    all_results = [analyze_file(str(f), threshold) for f in files_to_analyze]
    languages_found = {}
    for result in all_results:
        lang = result['language']
        if lang not in languages_found:
            languages_found[lang] = {'total': 0, 'vulnerable': 0}
        languages_found[lang]['total'] += 1
        if result['is_vulnerable']:
            languages_found[lang]['vulnerable'] += 1
    
    # Resumen
    print("="*70)
    print(f"RESUMEN: {len(vulnerable_files)}/{len(files_to_analyze)} archivos vulnerables")
    print("="*70)
    
    print(f"\n📊 Distribución por lenguaje:")
    for lang, stats in sorted(languages_found.items()):
        vuln_count = stats['vulnerable']
        total = stats['total']
        percentage = (vuln_count / total * 100) if total > 0 else 0
        status = "⚠️" if vuln_count > 0 else "✅"
        print(f"  {status} {lang}: {vuln_count}/{total} vulnerables ({percentage:.1f}%)")
    
    print("\n" + "="*70 + "\n")
    
    if vulnerable_files:
        print("⚠️  ALERTA: Se detectaron vulnerabilidades!")
        print("\nArchivos afectados:")
        for vf in vulnerable_files:
            lang_emoji = {
                'C': '🔵', 'C++': '🔷', 'Python': '🐍', 'Java': '☕',
                'JavaScript': '📜', 'TypeScript': '📘', 'PHP': '🐘',
                'Ruby': '💎', 'Go': '🔷'
            }.get(vf['language'], '📄')
            print(f"  {lang_emoji} [{vf['language']}] {vf['file']} ({vf['probability']*100:.1f}%)")
        sys.exit(1)  # Exit code 1 para fallar el pipeline
    else:
        print("✅ Todos los archivos pasaron la verificación de seguridad")
        sys.exit(0)


if __name__ == "__main__":
    main()
