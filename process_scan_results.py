#!/usr/bin/env python3
"""
Procesa resultados del scanner y genera outputs para GitHub Actions
"""

import argparse
import json
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Archivo JSON de resultados')
    parser.add_argument('--threshold', type=float, default=0.70, 
                       help='Umbral de probabilidad para considerar vulnerable')
    
    args = parser.parse_args()
    
    # Cargar resultados
    with open(args.input, 'r') as f:
        results = json.load(f)
    
    # Determinar si hay vulnerabilidades significativas
    has_vulnerabilities = any(
        v['probability'] >= args.threshold * 100
        for v in results.get('vulnerabilities', [])
    )
    
    # Set GitHub Actions output
    # https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"has_vulnerabilities={'true' if has_vulnerabilities else 'false'}\n")
            f.write(f"vulnerable_count={results.get('vulnerable', 0)}\n")
            f.write(f"safe_count={results.get('safe', 0)}\n")
    
    # Imprimir resumen
    print(f"Has vulnerabilities: {has_vulnerabilities}")
    print(f"Vulnerable files: {results.get('vulnerable', 0)}")
    print(f"Safe files: {results.get('safe', 0)}")
    
    sys.exit(0)

if __name__ == '__main__':
    main()
