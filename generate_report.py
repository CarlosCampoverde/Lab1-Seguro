"""
Genera reportes HTML con explicaciones SHAP
Para el pipeline CI/CD de detección de vulnerabilidades
"""

import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para CI/CD
import matplotlib.pyplot as plt
import shap
from pathlib import Path
import re
from datetime import datetime

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
DANGEROUS_FUNCTIONS_BY_LANG = {
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

DANGEROUS_FUNCTIONS = DANGEROUS_FUNCTIONS_BY_LANG['C']  # Para backward compatibility

def detect_language_from_code(code, file_extension=None):
    """Detecta el lenguaje de programación basado en patrones de código."""
    if file_extension and file_extension in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[file_extension]
    
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
        return 'C'


def extract_features(code, language=None, file_extension=None):
    """Extrae características del código (mismo que predict_vulnerabilities.py y notebook)"""
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


def generate_shap_explanation(code_snippet, model, vectorizer, output_path='shap_explanation.png'):
    """Genera visualización SHAP para un código específico"""
    # Extraer features
    manual_features = extract_features(code_snippet).to_frame().T
    tfidf_matrix = vectorizer.transform([code_snippet])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(), 
        columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    )
    X = pd.concat([manual_features.reset_index(drop=True), tfidf_df], axis=1)
    
    # Crear explainer SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Generar gráfico
    plt.figure(figsize=(12, 6))
    shap.summary_plot(shap_values, X, max_display=15, show=False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return shap_values, X


def generate_html_report():
    """Genera reporte HTML completo con resultados del análisis"""
    
    # Cargar modelos
    model = joblib.load('xgboost_vulnerabilidades.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    
    # Buscar archivos de todos los lenguajes soportados
    files_to_analyze = []
    for ext in SUPPORTED_LANGUAGES.keys():
        files_to_analyze.extend(list(Path('.').rglob(f'*{ext}')))
    files_to_analyze = [f for f in files_to_analyze if '.git' not in str(f)]
    
    if not files_to_analyze:
        supported_exts = ', '.join(SUPPORTED_LANGUAGES.keys())
        print(f"No se encontraron archivos para analizar")
        print(f"Extensiones soportadas: {supported_exts}")
        return
    
    # Analizar cada archivo
    results = []
    language_stats = {}
    
    for file_path in files_to_analyze:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Detectar lenguaje
            file_extension = file_path.suffix.lower()
            language = detect_language_from_code(code, file_extension)
            
            # Estadísticas por lenguaje
            if language not in language_stats:
                language_stats[language] = {'total': 0, 'vulnerable': 0}
            language_stats[language]['total'] += 1
            
            # Extraer features
            manual_features = extract_features(code, language, file_extension).to_frame().T
            tfidf_matrix = vectorizer.transform([code])
            tfidf_df = pd.DataFrame(
                tfidf_matrix.toarray(), 
                columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
            )
            X = pd.concat([manual_features.reset_index(drop=True), tfidf_df], axis=1)
            
            # Predicción
            probability = model.predict_proba(X)[0][1]
            prediction = "VULNERABLE" if probability > 0.7 else "SEGURO"
            
            if prediction == "VULNERABLE":
                language_stats[language]['vulnerable'] += 1
            
            # SHAP (solo para archivos vulnerables)
            shap_img = None
            if probability > 0.7:
                shap_path = f"shap_{file_path.stem}.png"
                generate_shap_explanation(code, model, vectorizer, shap_path)
                shap_img = shap_path
            
            results.append({
                'file': str(file_path),
                'language': language,
                'prediction': prediction,
                'probability': probability,
                'shap_img': shap_img,
                'lines': code.count('\n') + 1,
                'dangerous_funcs': manual_features['func_peligrosas'].values[0]
            })
            
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            continue
    
    # Ordenar por probabilidad descendente
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    # Generar HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Vulnerabilidades - Pipeline CI/CD</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 30px;
                background: #f8f9fa;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            .stat-label {{
                color: #666;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .results {{
                padding: 30px;
            }}
            .file-card {{
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 25px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }}
            .file-card:hover {{
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }}
            .file-card.vulnerable {{
                border-color: #dc3545;
                background: #fff5f5;
            }}
            .file-card.safe {{
                border-color: #28a745;
                background: #f5fff5;
            }}
            .file-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .file-name {{
                font-size: 1.2em;
                font-weight: bold;
                color: #333;
            }}
            .badge {{
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.9em;
            }}
            .badge.vulnerable {{
                background: #dc3545;
                color: white;
            }}
            .badge.safe {{
                background: #28a745;
                color: white;
            }}
            .probability-bar {{
                width: 100%;
                height: 30px;
                background: #e0e0e0;
                border-radius: 15px;
                overflow: hidden;
                margin: 15px 0;
            }}
            .probability-fill {{
                height: 100%;
                background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%);
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding-right: 10px;
                color: white;
                font-weight: bold;
                transition: width 0.5s ease;
            }}
            .metadata {{
                display: flex;
                gap: 20px;
                margin-top: 15px;
                color: #666;
                font-size: 0.9em;
            }}
            .shap-section {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
            }}
            .shap-section h3 {{
                color: #667eea;
                margin-bottom: 15px;
            }}
            .shap-section img {{
                width: 100%;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .footer {{
                background: #2a5298;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Reporte de Seguridad</h1>
                <p>Análisis de Vulnerabilidades - Pipeline CI/CD</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
            
            <div class="summary">
                <div class="stat-card">
                    <div class="stat-label">Archivos Analizados</div>
                    <div class="stat-value">{len(results)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Lenguajes</div>
                    <div class="stat-value" style="color: #667eea;">{len(language_stats)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Vulnerables</div>
                    <div class="stat-value" style="color: #dc3545;">
                        {sum(1 for r in results if r['probability'] > 0.7)}
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Seguros</div>
                    <div class="stat-value" style="color: #28a745;">
                        {sum(1 for r in results if r['probability'] <= 0.7)}
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Modelo</div>
                    <div class="stat-value" style="font-size: 1.5em;">XGBoost</div>
                </div>
            </div>
    """
    
    # Generar tarjetas de estadísticas por lenguaje
    lang_emojis = {"C": "🔵", "C++": "🔷", "Python": "🐍", "Java": "☕", "JavaScript": "📜", "TypeScript": "📘", "PHP": "🐘", "Ruby": "💎", "Go": "🔷"}
    lang_cards_html = ""
    for lang, stats in sorted(language_stats.items()):
        emoji = lang_emojis.get(lang, "📄")
        color = "#dc3545" if stats["vulnerable"] > 0 else "#28a745"
        percentage = (stats["vulnerable"]/stats["total"]*100)
        lang_cards_html += f'''
                    <div class="stat-card" style="text-align: left;">
                        <div style="font-size: 1.5em; margin-bottom: 10px;">
                            {emoji} {lang}
                        </div>
                        <div style="color: #666; font-size: 0.9em;">
                            Total: {stats["total"]} archivos
                        </div>
                        <div style="color: {color}; font-weight: bold;">
                            Vulnerables: {stats["vulnerable"]} ({percentage:.1f}%)
                        </div>
                    </div>
        '''
    
    # Continuar HTML
    html += f"""
            
            <div class="results">
                <h2 style="margin-bottom: 20px; color: #2a5298;">📊 Estadísticas por Lenguaje</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 30px;">
                    {lang_cards_html}
                </div>
                
                <h2 style="margin-bottom: 20px; color: #1e3c72;">📄 Resultados Detallados</h2>
    """
    
    # Agregar cada archivo
    for result in results:
        is_vulnerable = result['probability'] > 0.7
        card_class = 'vulnerable' if is_vulnerable else 'safe'
        badge_class = 'vulnerable' if is_vulnerable else 'safe'
        badge_text = '🚨 VULNERABLE' if is_vulnerable else '✅ SEGURO'
        
        # Emoji por lenguaje
        lang_emoji = {
            'C': '🔵', 'C++': '🔷', 'Python': '🐍', 'Java': '☕',
            'JavaScript': '📜', 'TypeScript': '📘', 'PHP': '🐘',
            'Ruby': '💎', 'Go': '🔷'
        }.get(result.get('language', 'Unknown'), '📄')
        
        html_content += f"""
                <div class="file-card {card_class}">
                    <div class="file-header">
                        <div class="file-name">{lang_emoji} [{result.get('language', 'Unknown')}] {result['file']}</div>
                        <div class="badge {badge_class}">{badge_text}</div>
                    </div>
                    
                    <div class="probability-bar">
                        <div class="probability-fill" style="width: {result['probability']*100}%">
                            {result['probability']*100:.1f}%
                        </div>
                    </div>
                    
                    <div class="metadata">
                        <span>💻 Lenguaje: {result.get('language', 'Unknown')}</span>
                        <span>📏 Líneas: {result['lines']}</span>
                        <span>⚠️ Funciones peligrosas: {result['dangerous_funcs']}</span>
                        <span>🎯 Confianza: {result['probability']*100:.2f}%</span>
                    </div>
        """
        
        # Agregar explicación SHAP si existe
        if result['shap_img']:
            html_content += f"""
                    <div class="shap-section">
                        <h3>🔍 Explicación SHAP - Features más influyentes</h3>
                        <img src="{result['shap_img']}" alt="SHAP Explanation">
                        <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                            Este gráfico muestra las características del código que más influyeron en la predicción.
                            Las barras rojas aumentan la probabilidad de vulnerabilidad, las azules la disminuyen.
                        </p>
                    </div>
            """
        
        html_content += """
                </div>
        """
    
    html_content += f"""
            </div>
            
            <div class="footer">
                <p><strong>Metodología SEMMA</strong> | Modelo: XGBoost con {500} estimadores</p>
                <p style="margin-top: 5px;">Pipeline CI/CD - Laboratorio Software Seguro</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Guardar HTML
    with open('vulnerability_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Reporte HTML generado: vulnerability_report.html")
    print(f"📊 Archivos analizados: {len(results)}")
    print(f"🚨 Vulnerables: {sum(1 for r in results if r['probability'] > 0.7)}")


if __name__ == "__main__":
    generate_html_report()
