#!/usr/bin/env python3
"""
🚀 PASO 1 SIMPLIFICADO: Mejorar Accuracy solo con XGBoost Optimizado
Sin dependencias complejas - Solo mejora del modelo actual
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 MEJORA DE ACCURACY - XGBoost Optimizado")
print("="*70)

# 1. CARGAR MODELO EXISTENTE
print("\n📥 Cargando modelo y datos existentes...")
try:
    model_old = joblib.load('xgboost_vulnerabilidades.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print(f"✅ Modelo actual cargado: {model_old.n_features_in_} features")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Ejecuta el notebook Lab1_SEMMA_Software_Seguro.ipynb primero")
    exit(1)

# 2. CARGAR DATASET
print("\n📥 Cargando dataset...")
if os.path.exists('diversevul.csv'):
    data = pd.read_csv('diversevul.csv', encoding='utf-8', on_bad_lines='skip', low_memory=False)
elif os.path.exists('diversevul.json'):
    data = pd.read_json('diversevul.json', lines=True)
else:
    print("❌ Dataset no encontrado")
    print("   Ejecuta el notebook primero")
    exit(1)

# Limpiar datos
data = data.dropna(subset=['func', 'target'])
print(f"✅ Dataset: {len(data):,} ejemplos")

# 3. USAR **TODO** EL DATASET DISPONIBLE (no solo 37K)
print("\n🚀 ESTRATEGIA: Usar MÁXIMOS datos disponibles")
n_vulnerable = (data['target']==1).sum()
n_safe = (data['target']==0).sum()

print(f"   Disponibles: {n_vulnerable:,} vulnerables, {n_safe:,} seguros")

# Tomar cantidad óptima balanceada (evitar out-of-memory)
n_use = min(n_vulnerable, n_safe, 12000)  # Máximo 12K por clase = 24K total
print(f"   Usando: {n_use:,} de cada clase = {n_use*2:,} TOTAL (optimizado para memoria)")

vulnerable = data[data['target']==1].sample(n=n_use, random_state=42)
safe = data[data['target']==0].sample(n=n_use, random_state=42)
data_balanced = pd.concat([vulnerable, safe]).sample(frac=1, random_state=42).reset_index(drop=True)

print(f"✅ Dataset balanceado: {len(data_balanced):,} ejemplos")

# 4. EXTRACT FEATURES
print("\n⚙️  Extrayendo features (esto puede tomar varios minutos)...")
from predict_vulnerabilities import extract_features

manual = data_balanced['func'].apply(extract_features)
print("   ✅ Features manuales: 30")

# TF-IDF
tfidf_matrix = vectorizer.transform(data_balanced['func'])
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
)
print(f"   ✅ Features TF-IDF: {tfidf_df.shape[1]}")

# Combinar
X = pd.concat([manual.reset_index(drop=True), tfidf_df], axis=1)
y = data_balanced['target']
print(f"✅ Total features: {X.shape[1]:,}")

# 5. SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 División:")
print(f"   Train: {len(X_train):,} ejemplos")
print(f"   Test: {len(X_test):,} ejemplos")

# 6. XGBOOST OPTIMIZADO (MEMORIA EFICIENTE)
print("\n🤖 Entrenando XGBoost OPTIMIZADO (memoria eficiente)...")
print("   (Esto puede tomar 3-5 minutos...)\n")

model_new = XGBClassifier(
    # HIPERPARÁMETROS OPTIMIZADOS - Balance accuracy/memoria
    n_estimators=1000,          # 1000 árboles (reduce memoria)
    max_depth=12,               # Profundidad moderada
    learning_rate=0.05,         # Learning rate moderado
    subsample=0.9,              # 90% de datos por árbol
    colsample_bytree=0.9,       # 90% de features por árbol
    min_child_weight=1,         # Permite hojas pequeñas
    gamma=0.1,                  # Poda moderada
    reg_alpha=0.1,              # L1 regularization
    reg_lambda=1.0,             # L2 regularization
    scale_pos_weight=1.0,       # Balanceado 50/50
    random_state=42,
    n_jobs=-1,
    tree_method='hist',         # Más eficiente en memoria
    max_bin=256,                # Reduce uso de memoria
    eval_metric='logloss',
    verbosity=1                 # Ver progreso
)

print("   Configuración:")
print(f"   • {model_new.n_estimators} árboles")
print(f"   • Profundidad: {model_new.max_depth}")
print(f"   • Learning rate: {model_new.learning_rate}")
print(f"   • Datos entrenamiento: {len(X_train):,}\n")

model_new.fit(X_train, y_train)

# 7. EVALUAR
print("\n📊 Evaluando modelo...")
y_pred = model_new.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*70)
print(f"🎯 ACCURACY NUEVO MODELO: {accuracy*100:.2f}%")
print("="*70)

print("\n" + classification_report(y_test, y_pred, target_names=['Seguro', 'Vulnerable']))

# 8. COMPARAR CON MODELO ANTERIOR
try:
    # Predecir con modelo anterior
    y_pred_old = model_old.predict(X_test)
    accuracy_old = accuracy_score(y_test, y_pred_old)
    
    print(f"\n📈 COMPARACIÓN:")
    print(f"   Modelo ANTERIOR: {accuracy_old*100:.2f}%")
    print(f"   Modelo NUEVO:    {accuracy*100:.2f}%")
    print(f"   Mejora:          +{(accuracy-accuracy_old)*100:.2f}%")
except:
    print(f"\n   (No se pudo comparar con modelo anterior)")

# 9. GUARDAR
if accuracy >= 0.82:
    print(f"\n✅ ¡OBJETIVO CUMPLIDO! Accuracy: {accuracy*100:.2f}% >= 82%")
    joblib.dump(model_new, 'xgboost_vulnerabilidades.pkl')
    print("💾 Modelo guardado: xgboost_vulnerabilidades.pkl")
    
    metadata = {
        'model_type': 'XGBoost',
        'accuracy': accuracy,
        'n_features': model_new.n_features_in_,
        'training_samples': len(X_train),
        'n_estimators': model_new.n_estimators,
        'max_depth': model_new.max_depth
    }
    joblib.dump(metadata, 'model_metadata.pkl')
    print("📋 Metadata guardada: model_metadata.pkl")
    
elif accuracy > accuracy_old if 'accuracy_old' in locals() else accuracy >= 0.75:
    print(f"\n✅ Modelo mejorado: {accuracy*100:.2f}%")
    if accuracy < 0.82:
        print(f"⚠️  Necesitas +{(0.82-accuracy)*100:.1f}% para llegar a 82%")
    
    print("\n¿Guardar este modelo mejorado? (s/n):", end=" ")
    try:
        respuesta = input().strip().lower()
        if respuesta == 's':
            joblib.dump(model_new, 'xgboost_vulnerabilidades.pkl')
            print(f"💾 Modelo guardado con {accuracy*100:.2f}% accuracy")
            
            metadata = {
                'model_type': 'XGBoost',
                'accuracy': accuracy,
                'n_features': model_new.n_features_in_,
                'training_samples': len(X_train)
            }
            joblib.dump(metadata, 'model_metadata.pkl')
    except:
        print("\nGuardando modelo automáticamente...")
        joblib.dump(model_new, 'xgboost_vulnerabilidades.pkl')
        print(f"💾 Modelo guardado")
else:
    print(f"\n⚠️  Accuracy {accuracy*100:.2f}% - considera usar más datos")

print("\n" + "="*70)
print("✅ PASO 1 COMPLETADO")
print("="*70)
print("\n💡 Próximo paso: Configurar Telegram Bot (QUICKSTART.md Paso 2)")
