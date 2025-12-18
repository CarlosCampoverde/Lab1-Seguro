# 🧪 GUÍA: Cómo Probar el Pipeline de Seguridad

## 🎯 Objetivo
Demostrar cómo el pipeline detecta vulnerabilidades automáticamente cuando subes código.

---

## 📋 MÉTODO 1: Crear Pull Request (Recomendado)

### Paso 1: Crear código en rama `dev`

```powershell
# Asegúrate de estar en dev
git checkout dev

# Crear archivo vulnerable
# Ya lo creé para ti: ejemplo_para_probar.c
git add ejemplo_para_probar.c
git commit -m "feat: Añadir código para probar scanner"
git push origin dev
```

### Paso 2: Crear Pull Request en GitHub

1. Ve a tu repositorio: https://github.com/CarlosCampoverde/Lab1-Seguro
2. Click en **"Pull requests"** → **"New pull request"**
3. Configurar:
   - **Base**: `test` (la rama destino)
   - **Compare**: `dev` (tu rama con el código)
4. Click **"Create pull request"**
5. Título: "Test: Verificar detección de vulnerabilidades"
6. Click **"Create pull request"**

### Paso 3: Ver el Workflow Ejecutándose

1. El workflow se dispara **automáticamente**
2. Ve a la pestaña **"Actions"**: https://github.com/CarlosCampoverde/Lab1-Seguro/actions
3. Verás el workflow "Security Pipeline" ejecutándose

### Paso 4: Ver los Resultados

El workflow tiene 4 jobs:

#### 🔍 Job 1: **security-scan**
```
✅ Analiza archivos .c, .cpp, .py, .java, etc.
✅ Usa el modelo XGBoost para predecir vulnerabilidades
✅ Genera scan_results.json
```

**Ejemplo de salida**:
```json
{
  "vulnerabilities": [
    {
      "file": "ejemplo_para_probar.c",
      "vulnerable": true,
      "probability": 0.92,
      "cwe_type": "CWE-120",
      "description": "Buffer overflow detected: strcpy, gets, sprintf"
    }
  ]
}
```

#### 🧪 Job 2: **tests**
```
✅ Ejecuta tests unitarios
✅ Verifica que el scanner funciona
```

#### 🔔 Job 3: **Notificación Telegram**
```
✅ Si hay vulnerabilidades → Envía alerta 🚨
✅ Si está limpio → Envía confirmación ✅
```

#### 🚀 Job 4: **deploy-production** (solo si es a main)
```
Solo se ejecuta en merge a main
```

### Paso 5: Ver Resultados Detallados

En la pestaña Actions → Click en tu workflow → Click en "security-scan":

Verás algo como:
```
🔍 Scanning files...
Found 1 files to scan:
  - ejemplo_para_probar.c

⚠️  VULNERABILITY DETECTED!
File: ejemplo_para_probar.c
Probability: 92.5%
CWE: CWE-120 (Buffer Overflow)
Dangerous functions: strcpy, gets, sprintf, system

Recommendation: Use safe alternatives (strncpy, fgets, snprintf)
```

---

## 📋 MÉTODO 2: Probar Localmente (Sin GitHub)

### Opción A: Usar el Scanner Directamente

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Analizar un archivo
python ci_security_scanner.py

# Verás la salida en scan_results.json
Get-Content scan_results.json | ConvertFrom-Json
```

### Opción B: Usar la API (Si está deployada)

```powershell
# Test de salud
Invoke-WebRequest -Uri "http://localhost:8080/health"

# Analizar archivo
$body = @{
    code = Get-Content ejemplo_para_probar.c -Raw
    language = "c"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/analyze" -Method POST -Body $body -ContentType "application/json"
```

### Opción C: Ejecutar Workflow Localmente

```powershell
# Instalar act (GitHub Actions local)
# Requiere Docker instalado
act pull_request -j security-scan
```

---

## 📋 MÉTODO 3: Ver Ejemplo Ya Existente

Ya creé un Pull Request de demostración anteriormente:

1. Ve a: https://github.com/CarlosCampoverde/Lab1-Seguro/pulls?q=is%3Apr
2. Busca PRs cerrados
3. Click en cualquier PR de "demo" o "test"
4. Ve a la pestaña **"Checks"**
5. Verás los resultados del scanner

---

## 🎯 ARCHIVOS DE PRUEBA INCLUIDOS

### ✅ Archivo VULNERABLE (debe ser detectado)
**Archivo**: `ejemplo_para_probar.c`

**Contiene**:
- ❌ `strcpy()` - Buffer overflow
- ❌ `gets()` - Buffer overflow garantizado
- ❌ `system()` - Command injection
- ❌ `sprintf()` - Format string
- ❌ SQL injection pattern

**Resultado esperado**: 
```
⚠️ VULNERABLE - Probability: 85-95%
```

### ✅ Archivo SEGURO (debe pasar)
**Archivo**: `ejemplo_seguro.c`

**Contiene**:
- ✅ `strncpy()` - Safe
- ✅ `fgets()` - Safe
- ✅ Input validation
- ✅ Whitelist approach
- ✅ Size checks

**Resultado esperado**: 
```
✅ SAFE - Probability: 10-20%
```

---

## 📊 RESULTADOS QUE VERÁS

### Si el código ES VULNERABLE:

#### En GitHub Actions:
```
❌ security-scan - Failed
   ⚠️ Vulnerabilities detected in 1 file(s)
   
❌ Workflow fails
   The PR is blocked from merging
```

#### En Telegram:
```
🚨 ALERTA DE SEGURIDAD

Repositorio: Lab1-Seguro
PR #5: Test vulnerabilidades

⚠️ Vulnerabilidades detectadas:
- ejemplo_para_probar.c (92% vulnerable)
  CWE-120: Buffer Overflow
  
Funciones peligrosas: strcpy, gets, system

🔗 Ver detalles: [link al PR]
```

### Si el código ES SEGURO:

#### En GitHub Actions:
```
✅ security-scan - Passed
   ✅ No vulnerabilities detected
   
✅ tests - Passed
   All 5 tests passed
   
✅ Workflow completes successfully
```

#### En Telegram:
```
✅ ANÁLISIS COMPLETADO

Repositorio: Lab1-Seguro
PR #6: Código seguro

✅ No se detectaron vulnerabilidades
✅ Tests: 5/5 passing

El código es seguro para merge.

🔗 Ver PR: [link]
```

---

## 🚀 PRUEBA RÁPIDA (5 minutos)

### Opción Más Rápida - Crear PR Ahora:

```powershell
# Desde tu terminal
git checkout dev
git add ejemplo_para_probar.c
git commit -m "test: Probar detección de vulnerabilidades"
git push origin dev

# Luego en navegador:
# 1. Ir a GitHub
# 2. Crear PR de dev → test
# 3. Ver Actions ejecutarse
# 4. Ver resultados en ~2 minutos
```

**Eso es todo**. El pipeline hace todo automáticamente.

---

## 📸 CAPTURAS IMPORTANTES

Para tu presentación, toma screenshots de:

1. **Pull Request creado**
   - URL: https://github.com/CarlosCampoverde/Lab1-Seguro/pulls

2. **Workflow ejecutándose**
   - URL: https://github.com/CarlosCampoverde/Lab1-Seguro/actions
   - Captura los 4 jobs en progreso

3. **Resultados del scan**
   - Click en "security-scan" job
   - Captura los logs con vulnerabilidades detectadas

4. **Notificación Telegram**
   - Captura el mensaje en tu chat de Telegram

5. **Tests pasando**
   - Captura los 5 tests en verde

6. **API Deployada** (si Render está listo)
   - Captura el `/health` endpoint respondiendo

---

## ❓ Troubleshooting

### El workflow no se ejecuta
- Verifica que el PR es a la rama `test`
- El workflow solo se dispara con PRs a `test`

### No veo vulnerabilidades
- Verifica que el archivo tiene extensión .c, .cpp, .py, etc.
- El scanner solo analiza archivos de código

### Telegram no envía mensajes
- Verifica GitHub Secrets (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
- Los secrets están configurados correctamente

---

## ✅ LISTO

Ahora puedes demostrar cómo funciona todo el pipeline de principio a fin.

**¿Quieres que creemos el PR ahora mismo para verlo en acción?**
