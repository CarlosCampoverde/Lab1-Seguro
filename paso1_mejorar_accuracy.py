#!/usr/bin/env python3
"""
🚀 PASO 1: Mejorar Accuracy del Modelo a 82%+
Script SIMPLIFICADO que carga datos directamente
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 MEJORA DE ACCURACY: Objetivo 82%+")
print("="*70)

# 1. CARGAR MODELO Y DATOS EXISTENTES
print("\n📥 Cargando modelo y vectorizador existentes...")
try:
    model_original = joblib.load('xgboost_vulnerabilidades.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print(f"✅ Modelo cargado: {model_original.n_features_in_} features")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Ejecuta primero el notebook Lab1_SEMMA_Software_Seguro.ipynb")
    print("   Específicamente la celda #VSC-a7dff439 (última celda)")
    exit(1)

# 2. CARGAR DATASET
print("\n📥 Cargando dataset DiverseVul...")
try:
    if os.path.exists('diversevul.csv'):
        data = pd.read_csv('diversevul.csv', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        print(f"✅ Dataset cargado: {len(data):,} ejemplos")
    else:
        print("❌ diversevul.csv no encontrado")
        print("   Ejecuta el notebook primero para descargar/procesar los datos")
        exit(1)
except Exception as e:
    print(f"❌ Error cargando datos: {e}")
    exit(1)

# 3. PREPARAR FEATURES (igual que en el notebook)
print("\n⚙️  Extrayendo features...")
from predict_vulnerabilities import extract_features

# Aplicar extract_features a todos los ejemplos
print("   Procesando features manuales...")
manual = data['func'].apply(extract_features)

# TF-IDF
print("   Generando TF-IDF...")
tfidf_matrix = vectorizer.transform(data['func'])
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
)

# Combinar
X = pd.concat([manual.reset_index(drop=True), tfidf_df], axis=1)
y = data['target']

print(f"✅ Features: {X.shape[1]:,} totales")
print(f"   Ejemplos: {len(X):,}")
print(f"   Vulnerable: {y.sum():,} ({y.sum()/len(y)*100:.1f}%)")

# 4. APLICAR SMOTE PARA BALANCE
print("\n🔄 Aplicando SMOTE...")
smote = SMOTE(random_state=42, k_neighbors=3)
X_resampled, y_resampled = smote.fit_resample(X, y)

print(f"   Después de SMOTE: {len(X_resampled):,} ejemplos")
print(f"   Balance: {(y_resampled==1).sum()/len(y_resampled)*100:.1f}% vulnerable")

# 5. SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled,
    test_size=0.2,
    random_state=42,
    stratify=y_resampled
)

print(f"\n📊 División:")
print(f"   Train: {len(X_train):,}")
print(f"   Test: {len(X_test):,}")

# 6. ENTRENAR ENSEMBLE
print("\n🤖 Entrenando ENSEMBLE (esto tomará varios minutos)...")

# Modelo 1: XGBoost MEJORADO
print("\n   [1/3] XGBoost OPTIMIZADO...")
xgb_model = XGBClassifier(
    n_estimators=1500,
    max_depth=15,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    min_child_weight=1,
    gamma=0.01,
    reg_alpha=0.01,
    reg_lambda=0.3,
    scale_pos_weight=1.0,
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss',
    verbosity=0
)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)
print(f"       ✅ XGBoost: {xgb_acc*100:.2f}%")

# Modelo 2: Random Forest
print("   [2/3] Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=1000,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1,
    verbose=0
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)
print(f"       ✅ Random Forest: {rf_acc*100:.2f}%")

# Modelo 3: LightGBM
print("   [3/3] LightGBM...")
lgb_model = lgb.LGBMClassifier(
    n_estimators=1500,
    max_depth=15,
    learning_rate=0.03,
    num_leaves=50,
    min_child_samples=20,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)
lgb_model.fit(X_train, y_train)
lgb_pred = lgb_model.predict(X_test)
lgb_acc = accuracy_score(y_test, lgb_pred)
print(f"       ✅ LightGBM: {lgb_acc*100:.2f}%")

# 7. ENSEMBLE (Voting)
print("\n🎯 Calculando ENSEMBLE (soft voting)...")
ensemble_pred_proba = (
    xgb_model.predict_proba(X_test) * 2 +
    rf_model.predict_proba(X_test) * 1 +
    lgb_model.predict_proba(X_test) * 1
) / 4
ensemble_pred = (ensemble_pred_proba[:, 1] > 0.5).astype(int)
ensemble_acc = accuracy_score(y_test, ensemble_pred)

# 8. RESULTADOS
print("\n" + "="*70)
print("📊 RESULTADOS FINALES")
print("="*70)
print(f"XGBoost:        {xgb_acc*100:.2f}%")
print(f"Random Forest:  {rf_acc*100:.2f}%")
print(f"LightGBM:       {lgb_acc*100:.2f}%")
print(f"ENSEMBLE:       {ensemble_acc*100:.2f}%")
print("="*70)

# Seleccionar mejor modelo
best_acc = max(xgb_acc, rf_acc, lgb_acc, ensemble_acc)
if best_acc == ensemble_acc:
    best_name = "ENSEMBLE"
    print(f"\n🏆 MEJOR: ENSEMBLE ({ensemble_acc*100:.2f}%)")
    
    # Crear wrapper para ensemble
    class EnsembleWrapper:
        def __init__(self, xgb, rf, lgb):
            self.xgb = xgb
            self.rf = rf
            self.lgb = lgb
            self.n_features_in_ = xgb.n_features_in_
        
        def predict(self, X):
            pred_proba = self.predict_proba(X)
            return (pred_proba[:, 1] > 0.5).astype(int)
        
        def predict_proba(self, X):
            return (
                self.xgb.predict_proba(X) * 2 +
                self.rf.predict_proba(X) * 1 +
                self.lgb.predict_proba(X) * 1
            ) / 4
    
    best_model = EnsembleWrapper(xgb_model, rf_model, lgb_model)
    
elif best_acc == xgb_acc:
    best_name = "XGBoost"
    best_model = xgb_model
    print(f"\n🏆 MEJOR: XGBoost ({xgb_acc*100:.2f}%)")
elif best_acc == rf_acc:
    best_name = "Random Forest"
    best_model = rf_model
    print(f"\n🏆 MEJOR: Random Forest ({rf_acc*100:.2f}%)")
else:
    best_name = "LightGBM"
    best_model = lgb_model
    print(f"\n🏆 MEJOR: LightGBM ({lgb_acc*100:.2f}%)")

# Report
print(f"\n📈 Classification Report ({best_name}):")
test_pred = best_model.predict(X_test) if best_name != "ENSEMBLE" else ensemble_pred
print(classification_report(y_test, test_pred, target_names=['Seguro', 'Vulnerable']))

# 9. GUARDAR
if best_acc >= 0.82:
    print(f"\n✅ ¡OBJETIVO CUMPLIDO! Accuracy >= 82%")
    joblib.dump(best_model, 'xgboost_vulnerabilidades.pkl')
    print("💾 Modelo guardado: xgboost_vulnerabilidades.pkl")
    
    metadata = {
        'model_type': best_name,
        'accuracy': best_acc,
        'n_features': best_model.n_features_in_,
        'training_samples': len(X_train),
        'balanced_with': 'SMOTE'
    }
    joblib.dump(metadata, 'model_metadata.pkl')
    print("📋 Metadata: model_metadata.pkl")
    
elif best_acc >= 0.75:
    print(f"\n✅ Accuracy mejorado a {best_acc*100:.2f}%")
    print(f"⚠️  Necesitas {(0.82-best_acc)*100:.1f}% más para llegar a 82%")
    
    save = input("\n¿Guardar este modelo mejorado? (s/n): ")
    if save.lower() == 's':
        joblib.dump(best_model, 'xgboost_vulnerabilidades.pkl')
        print(f"💾 Modelo guardado con {best_acc*100:.2f}% accuracy")
else:
    print(f"\n⚠️  Accuracy {best_acc*100:.2f}% aún bajo")
    print("\n💡 Para mejorar:")
    print("   1. Usa MÁS datos del dataset completo")
    print("   2. Agrega features de análisis estático (AST depth)")
    print("   3. Usa embeddings de CodeBERT")

print("\n" + "="*70)
print("✅ PASO 1 COMPLETADO")
print("="*70)
