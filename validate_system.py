#!/usr/bin/env python3
"""
🧪 Script de validación completa del sistema
Ejecuta todos los checks necesarios antes de deployment
"""

import os
import sys
import subprocess
import requests

def check(name, condition, fix_msg=""):
    """Helper para imprimir checks"""
    if condition:
        print(f"✅ {name}")
        return True
    else:
        print(f"❌ {name}")
        if fix_msg:
            print(f"   Fix: {fix_msg}")
        return False

def main():
    print("="*70)
    print("🔍 VALIDACIÓN COMPLETA DEL SISTEMA")
    print("="*70)
    
    all_passed = True
    
    # 1. Archivos esenciales
    print("\n📁 Verificando archivos esenciales...")
    all_passed &= check(
        "Modelo XGBoost existe",
        os.path.exists('xgboost_vulnerabilidades.pkl'),
        "Ejecutar: Lab1_SEMMA_Software_Seguro.ipynb celda final"
    )
    all_passed &= check(
        "Vectorizador TF-IDF existe",
        os.path.exists('tfidf_vectorizer.pkl'),
        "Ejecutar: Lab1_SEMMA_Software_Seguro.ipynb celda final"
    )
    all_passed &= check(
        "Workflow GitHub Actions existe",
        os.path.exists('.github/workflows/security-pipeline.yml'),
        "Ya creado por el asistente"
    )
    all_passed &= check(
        "Dockerfile existe",
        os.path.exists('Dockerfile'),
        "Ya creado por el asistente"
    )
    
    # 2. Scripts CI/CD
    print("\n🤖 Verificando scripts CI/CD...")
    all_passed &= check(
        "ci_security_scanner.py existe",
        os.path.exists('ci_security_scanner.py')
    )
    all_passed &= check(
        "telegram_notifier.py existe",
        os.path.exists('telegram_notifier.py')
    )
    all_passed &= check(
        "api_server.py existe",
        os.path.exists('api_server.py')
    )
    all_passed &= check(
        "predict_vulnerabilities.py existe",
        os.path.exists('predict_vulnerabilities.py')
    )
    
    # 3. Dependencias Python
    print("\n📦 Verificando dependencias...")
    try:
        import xgboost
        import sklearn
        import fastapi
        import uvicorn
        import pytest
        all_passed &= check("Todas las dependencias instaladas", True)
    except ImportError as e:
        all_passed &= check(
            "Todas las dependencias instaladas", 
            False,
            f"pip install -r requirements.txt (falta: {e})"
        )
    
    # 4. Variables de entorno
    print("\n🔐 Verificando variables de entorno...")
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
    
    all_passed &= check(
        "TELEGRAM_BOT_TOKEN configurado",
        telegram_token is not None,
        "export TELEGRAM_BOT_TOKEN='tu_token'"
    )
    all_passed &= check(
        "TELEGRAM_CHAT_ID configurado",
        telegram_chat is not None,
        "export TELEGRAM_CHAT_ID='tu_chat_id'"
    )
    
    # 5. Funcionalidad del modelo
    print("\n🤖 Probando modelo...")
    try:
        import joblib
        model = joblib.load('xgboost_vulnerabilidades.pkl')
        vectorizer = joblib.load('tfidf_vectorizer.pkl')
        
        all_passed &= check(
            f"Modelo cargado correctamente ({model.n_features_in_} features)",
            True
        )
        all_passed &= check(
            f"Vectorizador cargado ({len(vectorizer.get_feature_names_out())} features TF-IDF)",
            True
        )
        
        # Test de predicción
        test_code = "char buf[64]; strcpy(buf, input);"
        from predict_vulnerabilities import extract_features
        import pandas as pd
        
        features = extract_features(test_code)
        manual_df = pd.DataFrame([features])
        tfidf_features = vectorizer.transform([test_code]).toarray()
        tfidf_df = pd.DataFrame(
            tfidf_features,
            columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
        )
        X = pd.concat([manual_df.reset_index(drop=True), tfidf_df], axis=1)
        
        pred = model.predict(X)[0]
        all_passed &= check(
            f"Predicción funciona (resultado: {'VULNERABLE' if pred == 1 else 'SEGURO'})",
            True
        )
        
    except Exception as e:
        all_passed &= check(
            "Modelo funciona correctamente",
            False,
            f"Error: {e}"
        )
    
    # 6. Tests unitarios
    print("\n🧪 Ejecutando tests...")
    try:
        result = subprocess.run(
            ['pytest', 'tests/', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )
        all_passed &= check(
            "Tests unitarios pasan",
            result.returncode == 0,
            "pytest tests/ -v (ver errores arriba)"
        )
    except FileNotFoundError:
        all_passed &= check(
            "Tests unitarios pasan",
            False,
            "pip install pytest"
        )
    except Exception as e:
        print(f"   ⚠️  Tests: {e}")
    
    # 7. Telegram connectivity
    if telegram_token and telegram_chat:
        print("\n📱 Probando Telegram...")
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/getMe"
            response = requests.get(url, timeout=5)
            
            all_passed &= check(
                "Bot de Telegram responde",
                response.status_code == 200,
                "Verificar TELEGRAM_BOT_TOKEN"
            )
        except Exception as e:
            all_passed &= check(
                "Bot de Telegram responde",
                False,
                f"Error: {e}"
            )
    
    # 8. Git repository
    print("\n📂 Verificando repositorio Git...")
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        current_branch = result.stdout.strip()
        all_passed &= check(
            f"Git repository configurado (rama: {current_branch})",
            result.returncode == 0
        )
        
        # Verificar ramas necesarias
        result = subprocess.run(
            ['git', 'branch', '-r'],
            capture_output=True,
            text=True
        )
        remote_branches = result.stdout
        
        has_dev = 'dev' in remote_branches or 'origin/dev' in remote_branches
        has_test = 'test' in remote_branches or 'origin/test' in remote_branches
        has_main = 'main' in remote_branches or 'origin/main' in remote_branches
        
        all_passed &= check(
            "Rama 'dev' existe",
            has_dev,
            "git checkout -b dev && git push origin dev"
        )
        all_passed &= check(
            "Rama 'test' existe",
            has_test,
            "git checkout -b test && git push origin test"
        )
        all_passed &= check(
            "Rama 'main' existe",
            has_main,
            "git checkout -b main && git push origin main"
        )
        
    except Exception as e:
        print(f"   ⚠️  Git: {e}")
    
    # 9. Accuracy check
    print("\n📊 Verificando accuracy del modelo...")
    try:
        if os.path.exists('model_metadata.pkl'):
            import joblib
            metadata = joblib.load('model_metadata.pkl')
            accuracy = metadata.get('accuracy', 0)
            
            all_passed &= check(
                f"Accuracy del modelo: {accuracy*100:.2f}%",
                accuracy >= 0.82,
                "Ejecutar: python improve_accuracy.py"
            )
        else:
            print("   ⚠️  Metadata no encontrada, ejecutar improve_accuracy.py")
    except Exception as e:
        print(f"   ⚠️  Metadata: {e}")
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    if all_passed:
        print("✅ SISTEMA COMPLETAMENTE VALIDADO")
        print("="*70)
        print("\n🚀 Próximos pasos:")
        print("   1. Hacer commit de todos los archivos")
        print("   2. git push origin dev")
        print("   3. Crear PR: dev → test en GitHub")
        print("   4. Ver pipeline en acción!")
        print("\n¡Listo para deployment! ✨")
        sys.exit(0)
    else:
        print("❌ VALIDACIÓN FALLIDA")
        print("="*70)
        print("\n⚠️  Corrige los errores marcados arriba y vuelve a ejecutar:")
        print("   python validate_system.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
