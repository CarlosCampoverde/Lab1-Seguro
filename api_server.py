#!/usr/bin/env python3
"""
🚀 API REST para el Vulnerability Scanner
Desplegado en Render/Railway para producción
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import joblib
import pandas as pd
from datetime import datetime
import os

# Importar funciones del predictor
from predict_vulnerabilities import extract_features

app = FastAPI(
    title="🔒 Vulnerability Scanner API",
    description="API de detección de vulnerabilidades con ML (XGBoost)",
    version="1.0.0"
)

# CORS para permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo al inicio
print("🤖 Cargando modelo de ML...")
MODEL_PATH = os.getenv('MODEL_PATH', 'xgboost_vulnerabilidades.pkl')
VECTORIZER_PATH = os.getenv('VECTORIZER_PATH', 'tfidf_vectorizer.pkl')

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print(f"✅ Modelo cargado: {model.n_features_in_} features")
except Exception as e:
    print(f"❌ Error cargando modelo: {e}")
    model = None
    vectorizer = None

# Modelos Pydantic
class CodeAnalysisRequest(BaseModel):
    code: str
    language: Optional[str] = None
    filename: Optional[str] = None

class VulnerabilityResult(BaseModel):
    is_vulnerable: bool
    probability_vulnerable: float
    probability_safe: float
    confidence: float
    vulnerability_type: Optional[str] = None
    reason: Optional[str] = None
    features: dict
    timestamp: str

# Endpoints
@app.get("/")
async def root():
    """Endpoint raíz - Info de la API"""
    return {
        "name": "Vulnerability Scanner API",
        "version": "1.0.0",
        "status": "online" if model is not None else "model_not_loaded",
        "endpoints": {
            "/analyze": "POST - Analizar código",
            "/health": "GET - Health check",
            "/stats": "GET - Estadísticas del modelo"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para Docker/Render"""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    
    return {
        "status": "healthy",
        "model_loaded": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
async def get_stats():
    """Estadísticas del modelo"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    return {
        "model_type": "XGBoost Classifier",
        "features": model.n_features_in_,
        "languages_supported": ["C", "C++", "Python", "Java", "JavaScript", "PHP", "Ruby", "Go"],
        "accuracy": "71.34%",
        "training_dataset": "DiverseVul (37,890 examples)",
        "methodology": "SEMMA"
    }

@app.post("/analyze", response_model=VulnerabilityResult)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analiza código y detecta vulnerabilidades
    
    Body JSON:
    {
        "code": "código fuente aquí",
        "language": "python" (opcional),
        "filename": "test.py" (opcional)
    }
    """
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Extraer features manuales
        features_series = extract_features(request.code)
        manual_df = pd.DataFrame([features_series])
        
        # TF-IDF
        tfidf_features = vectorizer.transform([request.code]).toarray()
        tfidf_df = pd.DataFrame(
            tfidf_features,
            columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
        )
        
        # Combinar features
        X = pd.concat([manual_df.reset_index(drop=True), tfidf_df], axis=1)
        
        # Predicción
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Clasificar tipo de vulnerabilidad
        vulnerability_type = None
        reason = None
        
        if prediction == 1:
            if features_series['usa_strcpy'] or features_series['usa_gets']:
                vulnerability_type = 'Buffer Overflow (CWE-119)'
                reason = 'Uso de funciones inseguras de manejo de strings'
            elif features_series['usa_eval'] or features_series['usa_exec']:
                vulnerability_type = 'Code Injection (CWE-94)'
                reason = 'Uso de eval/exec permite ejecución arbitraria'
            elif features_series['func_peligrosas_python'] > 0:
                vulnerability_type = 'Insecure Deserialization (CWE-502)'
                reason = 'Deserialización insegura (pickle.loads)'
            else:
                vulnerability_type = 'Vulnerability Pattern Detected'
                reason = 'Patrón de código vulnerable detectado por IA'
        
        return VulnerabilityResult(
            is_vulnerable=bool(prediction == 1),
            probability_vulnerable=float(probabilities[1] * 100),
            probability_safe=float(probabilities[0] * 100),
            confidence=float(max(probabilities) * 100),
            vulnerability_type=vulnerability_type,
            reason=reason,
            features={
                'lines': int(features_series['lineas']),
                'length': int(features_series['longitud']),
                'dangerous_functions': int(features_series['total_peligrosas']),
                'complexity': int(features_series['complejidad_ciclomatica']),
                'has_sanitization': bool(features_series['sanitizacion'])
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@app.post("/batch-analyze")
async def batch_analyze(files: List[UploadFile] = File(...)):
    """Analiza múltiples archivos (para CI/CD)"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    results = []
    
    for file in files:
        try:
            code = await file.read()
            code_str = code.decode('utf-8')
            
            # Analizar
            analysis = await analyze_code(CodeAnalysisRequest(
                code=code_str,
                filename=file.filename
            ))
            
            results.append({
                "filename": file.filename,
                "result": analysis
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "total_files": len(files),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
