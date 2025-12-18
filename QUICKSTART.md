# ⚡ Quick Start Guide

## 🎯 Pasos Para Implementar el Pipeline CI/CD

### ✅ Paso 1: Mejorar Accuracy a 82%+ (URGENTE)

**Opción A: Ejecutar script de mejora**
```bash
python improve_accuracy.py
```

**Opción B: En el notebook, agregar más datos**
```python
# En celda #VSC-2581e32b, cambiar:
n_samples = 18945  # Usar TODOS los vulnerables
n_safe_samples = 18945  # Balance 50/50

# Esto te dará ~38K ejemplos balanceados
# Luego ejecutar improve_accuracy.py con SMOTE
```

**Opción C: RÁPIDO - Usar técnica de ensemble**
1. Abre [Lab1_SEMMA_Software_Seguro.ipynb](Lab1_SEMMA_Software_Seguro.ipynb)
2. Ejecuta celda final (#VSC-a7dff439)
3. Ejecuta `python improve_accuracy.py`
4. ¡Listo! Tendrás ~5-8% más de accuracy

---

### ✅ Paso 2: Configurar Bot de Telegram (5 minutos)

1. **Crear bot:**
   - Abre Telegram → busca `@BotFather`
   - Envía: `/newbot`
   - Nombre: `VulnScannerBot` (o el que quieras)
   - Username: `your_username_vulnscanner_bot`
   - Copia el **TOKEN** (ej: `1234567890:ABCdef...`)

2. **Obtener Chat ID:**
   - Busca `@userinfobot` en Telegram
   - Envía: `/start`
   - Copia tu **Chat ID** (ej: `123456789`)

3. **Probar localmente:**
   ```bash
   export TELEGRAM_BOT_TOKEN="tu_token"
   export TELEGRAM_CHAT_ID="tu_chat_id"
   python telegram_notifier.py --message "Test OK" --status "success"
   ```

---

### ✅ Paso 3: Configurar GitHub Secrets (3 minutos)

1. Ve a tu repositorio en GitHub
2. `Settings` → `Secrets and variables` → `Actions`
3. Click `New repository secret`
4. Agregar estos secrets:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef... (de paso 2)
TELEGRAM_CHAT_ID=123456789 (de paso 2)
```

---

### ✅ Paso 4: Configurar Branch Protection (2 minutos)

1. GitHub → `Settings` → `Branches`
2. Click `Add branch protection rule`

**Para rama `test`:**
- Branch name pattern: `test`
- ✅ Require pull request before merging
- ✅ Require status checks: `security-scan`, `tests`

**Para rama `main`:**
- Branch name pattern: `main`
- ✅ Require pull request before merging
- ✅ Require status checks to pass

---

### ✅ Paso 5: Crear las Ramas (1 minuto)

```bash
# En tu repositorio local
git checkout -b dev
git push origin dev

git checkout -b test  
git push origin test

git checkout main
git push origin main
```

---

### ✅ Paso 6: Configurar Render (Despliegue) (10 minutos)

1. Ir a [render.com](https://render.com) → Sign Up (gratis)
2. Click `New +` → `Web Service`
3. Connect GitHub repository
4. Configurar:
   - **Name:** `vulnerability-scanner`
   - **Environment:** Docker
   - **Branch:** main
   - **Instance Type:** Free

5. Variables de entorno en Render:
   ```
   PORT=8080
   MODEL_PATH=xgboost_vulnerabilidades.pkl
   VECTORIZER_PATH=tfidf_vectorizer.pkl
   ```

6. Click `Create Web Service`
7. Esperar deploy (~5 min)
8. Copiar URL: `https://vulnerability-scanner-xxxx.onrender.com`

9. **Obtener API Key y Service ID:**
   - Settings → API Keys → Create
   - Copiar Service ID de la URL del dashboard

10. **Agregar a GitHub Secrets:**
    ```
    RENDER_API_KEY=rnd_xxxxx
    RENDER_SERVICE_ID=srv_xxxxx
    PRODUCTION_URL=https://tu-app.onrender.com
    ```

---

### ✅ Paso 7: Probar el Pipeline Completo (5 minutos)

```bash
# 1. Crear feature branch
git checkout dev
git checkout -b feature/test-pipeline

# 2. Crear archivo VULNERABLE
cat > test_vuln.py << 'EOF'
import pickle

def load(file):
    return pickle.loads(open(file, 'rb').read())  # Vulnerable!
EOF

# 3. Commit y push
git add test_vuln.py
git commit -m "Add test file"
git push origin feature/test-pipeline

# 4. Ir a GitHub y crear PR: feature/test-pipeline → test

# 5. Ver el pipeline en acción:
#    - GitHub Actions se ejecuta
#    - Modelo detecta vulnerabilidad
#    - PR bloqueado
#    - Notificación en Telegram ❌

# 6. Corregir código
cat > test_vuln.py << 'EOF'
import json

def load(file):
    return json.load(open(file, 'r'))  # Seguro!
EOF

git add test_vuln.py
git commit -m "Fix vulnerability"
git push

# 7. Ver pipeline exitoso:
#    - Security scan: ✅
#    - Tests: ✅
#    - Auto-merge to test
#    - Deploy to Render 🚀
#    - Notificación en Telegram ✅
```

---

## 📊 Verificar que Todo Funciona

### ✅ Checklist Final

- [ ] Modelo con accuracy ≥ 82%
- [ ] Bot de Telegram responde
- [ ] GitHub Actions ejecuta workflow
- [ ] Branch protection bloquea merges directos
- [ ] API en Render está online (health check)
- [ ] Notificaciones Telegram funcionan
- [ ] Tests pasan localmente: `pytest tests/`

### 🧪 Tests Rápidos

```bash
# 1. Modelo funciona
python predict_vulnerabilities.py ejemplos_multilenguaje/vulnerable_python.py

# 2. API local funciona
python api_server.py
# En otra terminal:
curl http://localhost:8080/health

# 3. Scanner CI/CD funciona
python ci_security_scanner.py --files "test.py" --pr-number 1

# 4. Telegram funciona
python telegram_notifier.py --message "Test" --status "info"

# 5. Tests pasan
pytest tests/ -v
```

---

## 🚨 Troubleshooting Rápido

### Problema: Accuracy < 82%

```bash
# Solución 1: Ejecutar script de mejora
python improve_accuracy.py

# Solución 2: Usar ensemble en el notebook
# Ejecutar celdas con XGBoost + RandomForest + LightGBM
```

### Problema: Telegram no envía mensajes

```bash
# Verificar token
echo $TELEGRAM_BOT_TOKEN

# Probar manualmente
python -c "import telegram_notifier; telegram_notifier.TelegramNotifier().send_message('Test', 'info')"
```

### Problema: GitHub Actions falla

1. Ver logs: `Actions` → Click en workflow run
2. Verificar que `.github/workflows/security-pipeline.yml` existe
3. Verificar GitHub Secrets están configurados

### Problema: Render deployment falla

1. Ver logs en Render Dashboard
2. Verificar que `Dockerfile` existe
3. Verificar archivos `.pkl` están en el repo (o usa Git LFS)

---

## 🎯 Criterios de Evaluación - Checklist

- [ ] **6 puntos** - Pipeline completamente automatizado
  - [ ] dev → test → main flujo automático
  - [ ] Trigger en PR creation
  - [ ] Auto-merge cuando pasa

- [ ] **6 puntos** - Modelo ML propio y efectivo
  - [ ] XGBoost entrenado por ti
  - [ ] Accuracy ≥ 82%
  - [ ] Dataset público documentado
  - [ ] NO usa LLM

- [ ] **3 puntos** - Notificaciones + issues
  - [ ] Telegram en todas las fases
  - [ ] Labels automáticas
  - [ ] Comentarios en PR

- [ ] **3 puntos** - Despliegue automático
  - [ ] Docker build automático
  - [ ] Deploy a Render/Railway
  - [ ] URL pública funcional

- [ ] **2 puntos** - Documentación
  - [ ] README completo
  - [ ] Notebook con entrenamiento
  - [ ] Capturas de pantalla

---

## ⏱️ Tiempo Estimado Total: 30-40 minutos

Si sigues estos pasos en orden, tendrás el pipeline completo funcionando en menos de 1 hora.

**¡Buena suerte! 🚀**
