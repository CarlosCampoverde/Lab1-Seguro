#!/usr/bin/env python3
"""
🔒 CI Security Scanner con Modelo de Minería de Datos
Analiza archivos modificados en PR y detecta vulnerabilidades usando XGBoost
NO USA LLM - Solo ML tradicional
"""

import argparse
import json
import sys
import os
from pathlib import Path
import joblib
import pandas as pd
import re

# Importar funciones del predictor existente
from predict_vulnerabilities import extract_features, SUPPORTED_LANGUAGES

class CISecurityScanner:
    def __init__(self, model_path='xgboost_vulnerabilidades.pkl', 
                 vectorizer_path='tfidf_vectorizer.pkl'):
        """Inicializar scanner con modelo entrenado"""
        print(f"🤖 Cargando modelo de IA...")
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        print(f"✅ Modelo cargado: {self.model.n_features_in_} features")
        
    def scan_file(self, file_path):
        """
        Analiza un archivo individual y retorna resultado
        
        Returns:
            dict: {
                'file': str,
                'is_vulnerable': bool,
                'probability': float,
                'confidence': float,
                'details': dict
            }
        """
        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Detectar lenguaje
            ext = Path(file_path).suffix
            if ext not in SUPPORTED_LANGUAGES:
                return {
                    'file': file_path,
                    'skipped': True,
                    'reason': f'Extensión {ext} no soportada'
                }
            
            # Extraer features manuales
            features_series = extract_features(code)
            manual_df = pd.DataFrame([features_series])
            
            # TF-IDF
            tfidf_features = self.vectorizer.transform([code]).toarray()
            tfidf_df = pd.DataFrame(
                tfidf_features, 
                columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
            )
            
            # Combinar features
            X = pd.concat([manual_df.reset_index(drop=True), tfidf_df], axis=1)
            
            # Predicción
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            result = {
                'file': str(file_path),
                'language': SUPPORTED_LANGUAGES.get(ext, 'unknown'),
                'is_vulnerable': bool(prediction == 1),
                'probability_safe': float(probabilities[0] * 100),
                'probability_vulnerable': float(probabilities[1] * 100),
                'confidence': float(max(probabilities) * 100),
                'features': {
                    'lines': int(features_series['lineas']),
                    'dangerous_functions': int(features_series['total_peligrosas']),
                    'complexity': int(features_series['complejidad_ciclomatica']),
                    'has_sanitization': bool(features_series['sanitizacion'])
                }
            }
            
            # Análisis adicional si es vulnerable
            if result['is_vulnerable']:
                result['vulnerability_type'] = self._classify_vulnerability_type(features_series)
                result['reason'] = self._explain_vulnerability(features_series, code)
            
            return result
            
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'skipped': True
            }
    
    def _classify_vulnerability_type(self, features):
        """Clasifica el tipo de vulnerabilidad basado en features"""
        if features['usa_strcpy'] or features['usa_gets']:
            return 'Buffer Overflow (CWE-119)'
        elif features['usa_eval'] or features['usa_exec']:
            return 'Code Injection (CWE-94)'
        elif features['func_peligrosas_python'] > 0:
            return 'Insecure Deserialization (CWE-502)'
        elif features['func_peligrosas_js'] > 0:
            return 'Cross-Site Scripting (CWE-79)'
        elif features['func_peligrosas_java'] > 0:
            return 'Command Injection (CWE-78)'
        else:
            return 'Vulnerability Pattern Detected'
    
    def _explain_vulnerability(self, features, code):
        """Genera explicación de por qué es vulnerable"""
        reasons = []
        
        if features['total_peligrosas'] > 0:
            reasons.append(f"Detectadas {features['total_peligrosas']} funciones peligrosas")
        
        if features['usa_strcpy']:
            reasons.append("Uso de strcpy() sin límites de buffer")
        
        if features['usa_gets']:
            reasons.append("Uso de gets() (función prohibida)")
        
        if features['usa_eval']:
            reasons.append("Uso de eval() permite ejecución arbitraria")
        
        if not features['sanitizacion']:
            reasons.append("No se detectó sanitización de entrada")
        
        if features['complejidad_ciclomatica'] > 10:
            reasons.append(f"Alta complejidad ({features['complejidad_ciclomatica']}) dificulta revisión")
        
        return '; '.join(reasons) if reasons else 'Patrón de código vulnerable detectado por IA'
    
    def scan_multiple(self, file_paths):
        """Escanea múltiples archivos"""
        results = {
            'total_files': 0,
            'scanned': 0,
            'skipped': 0,
            'vulnerable': 0,
            'safe': 0,
            'files': []
        }
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                continue
                
            results['total_files'] += 1
            result = self.scan_file(file_path)
            results['files'].append(result)
            
            if result.get('skipped'):
                results['skipped'] += 1
            else:
                results['scanned'] += 1
                if result['is_vulnerable']:
                    results['vulnerable'] += 1
                else:
                    results['safe'] += 1
        
        # Resumen de vulnerabilidades
        results['vulnerabilities'] = [
            {
                'file': r['file'],
                'probability': r['probability_vulnerable'],
                'type': r.get('vulnerability_type', 'Unknown'),
                'reason': r.get('reason', ''),
                'line': 1  # TODO: implementar detección de línea específica
            }
            for r in results['files']
            if not r.get('skipped') and r.get('is_vulnerable')
        ]
        
        results['has_vulnerabilities'] = results['vulnerable'] > 0
        
        return results

def main():
    parser = argparse.ArgumentParser(
        description='🔒 Scanner de seguridad con IA para CI/CD'
    )
    parser.add_argument('--files', required=True, help='Archivos a escanear (separados por espacio)')
    parser.add_argument('--pr-number', help='Número de PR')
    parser.add_argument('--output-json', default='scan_results.json', help='Archivo de salida')
    parser.add_argument('--model', default='xgboost_vulnerabilidades.pkl', help='Ruta al modelo')
    parser.add_argument('--vectorizer', default='tfidf_vectorizer.pkl', help='Ruta al vectorizador')
    
    args = parser.parse_args()
    
    # Parsear archivos
    file_list = args.files.strip().split()
    
    print("="*70)
    print("🔒 CI/CD SECURITY SCANNER")
    print("="*70)
    print(f"📋 PR: #{args.pr_number if args.pr_number else 'N/A'}")
    print(f"📁 Archivos a analizar: {len(file_list)}")
    print("="*70)
    
    # Inicializar scanner
    scanner = CISecurityScanner(model_path=args.model, vectorizer_path=args.vectorizer)
    
    # Escanear archivos
    results = scanner.scan_multiple(file_list)
    
    # Guardar resultados
    with open(args.output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Imprimir resumen
    print(f"\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"   Total archivos: {results['total_files']}")
    print(f"   Escaneados: {results['scanned']}")
    print(f"   Omitidos: {results['skipped']}")
    print(f"   ✅ Seguros: {results['safe']}")
    print(f"   🚨 Vulnerables: {results['vulnerable']}")
    
    if results['has_vulnerabilities']:
        print(f"\n🚨 VULNERABILIDADES DETECTADAS:")
        for vuln in results['vulnerabilities']:
            print(f"   • {vuln['file']}: {vuln['type']} ({vuln['probability']:.1f}%)")
            print(f"     Razón: {vuln['reason']}")
        print("\n❌ ESCANEO FALLIDO - Código vulnerable detectado")
        sys.exit(1)
    else:
        print(f"\n✅ ESCANEO EXITOSO - Todo el código es seguro")
        sys.exit(0)

if __name__ == '__main__':
    main()
