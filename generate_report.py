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

DANGEROUS_FUNCTIONS = [
    'strcpy', 'gets', 'sprintf', 'strcat', 'scanf', 
    'system', 'exec', 'popen', 'memset', 'memcpy'
]

def extract_features(code):
    """Extrae características del código (mismo que predict_vulnerabilities.py)"""
    features = {}
    features['longitud'] = len(code)
    features['lineas'] = code.count('\n') + 1
    features['func_peligrosas'] = sum(code.count(func) for func in DANGEROUS_FUNCTIONS)
    features['usa_strcpy'] = int('strcpy' in code)
    features['usa_gets'] = int('gets' in code)
    features['usa_system'] = int('system' in code)
    
    security_patterns = ['sanitize', 'escape', 'check', 'validate', 'safe_str']
    features['sanitizacion'] = int(any(pattern in code.lower() for pattern in security_patterns))
    features['complejidad_ciclomatica'] = len(re.findall(r'\b(if|while|for|case|catch|&&|\|\|)\b', code))
    features['anidamiento'] = abs(code.count('{') - code.count('}'))
    
    return pd.Series(features)


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
    
    # Buscar archivos C/C++
    files_to_analyze = list(Path('.').rglob('*.c')) + list(Path('.').rglob('*.cpp'))
    files_to_analyze = [f for f in files_to_analyze if '.git' not in str(f)]
    
    if not files_to_analyze:
        print("No se encontraron archivos para analizar")
        return
    
    # Analizar cada archivo
    results = []
    for file_path in files_to_analyze:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Extraer features
            manual_features = extract_features(code).to_frame().T
            tfidf_matrix = vectorizer.transform([code])
            tfidf_df = pd.DataFrame(
                tfidf_matrix.toarray(), 
                columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
            )
            X = pd.concat([manual_features.reset_index(drop=True), tfidf_df], axis=1)
            
            # Predicción
            probability = model.predict_proba(X)[0][1]
            prediction = "VULNERABLE" if probability > 0.7 else "SEGURO"
            
            # SHAP (solo para archivos vulnerables)
            shap_img = None
            if probability > 0.7:
                shap_path = f"shap_{file_path.stem}.png"
                generate_shap_explanation(code, model, vectorizer, shap_path)
                shap_img = shap_path
            
            results.append({
                'file': str(file_path),
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
            
            <div class="results">
                <h2 style="margin-bottom: 20px; color: #1e3c72;">📊 Resultados Detallados</h2>
    """
    
    # Agregar cada archivo
    for result in results:
        is_vulnerable = result['probability'] > 0.7
        card_class = 'vulnerable' if is_vulnerable else 'safe'
        badge_class = 'vulnerable' if is_vulnerable else 'safe'
        badge_text = '🚨 VULNERABLE' if is_vulnerable else '✅ SEGURO'
        
        html_content += f"""
                <div class="file-card {card_class}">
                    <div class="file-header">
                        <div class="file-name">📄 {result['file']}</div>
                        <div class="badge {badge_class}">{badge_text}</div>
                    </div>
                    
                    <div class="probability-bar">
                        <div class="probability-fill" style="width: {result['probability']*100}%">
                            {result['probability']*100:.1f}%
                        </div>
                    </div>
                    
                    <div class="metadata">
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
