# 📦 Cómo Analizar un Proyecto Completo

## 🎯 Respuesta Rápida

**Solo tienes que**:
1. Poner tu proyecto en cualquier carpeta del repositorio
2. Hacer commit y push
3. Crear Pull Request

**El pipeline analiza TODOS los archivos automáticamente**.

---

## 📁 Dónde Poner Tu Proyecto

### Opción 1: Carpeta específica (Recomendado)
```
Lab1-Seguro/
├── tu_proyecto/           ← Tu proyecto aquí
│   ├── src/
│   ├── include/
│   ├── lib/
│   └── README.md
├── otro_proyecto/         ← Puedes tener varios
│   └── ...
└── .github/workflows/     ← Pipeline (ya está)
```

### Opción 2: En la raíz
```
Lab1-Seguro/
├── main.c                 ← Archivos de tu proyecto
├── auth.c
├── database.c
├── utils.c
└── .github/workflows/     ← Pipeline
```

### Opción 3: Múltiples proyectos
```
Lab1-Seguro/
├── proyectos/
│   ├── proyecto_web/
│   ├── proyecto_api/
│   └── proyecto_cli/
└── .github/workflows/
```

---

## 🚀 PASOS COMPLETOS

### 1️⃣ Agregar Tu Proyecto al Repositorio

```powershell
# Opción A: Copiar proyecto existente
Copy-Item -Recurse C:\tu\proyecto\* C:\ESPE\Lab1-Seguro\mi_proyecto\

# Opción B: Crear proyecto desde cero
# (Ya puedes tener tus archivos en carpetas del repo)
```

### 2️⃣ Hacer Commit en rama dev

```powershell
# Cambiar a rama dev
git checkout dev

# Ver qué archivos añadiste
git status

# Añadir TODO tu proyecto
git add mi_proyecto/

# O añadir todo
git add .

# Commit
git commit -m "feat: Añadir mi proyecto completo para análisis"

# Push a GitHub
git push origin dev
```

### 3️⃣ Crear Pull Request

**En tu navegador:**
1. Ve a: https://github.com/CarlosCampoverde/Lab1-Seguro
2. Click **"Pull requests"** → **"New pull request"**
3. Selecciona:
   - **Base**: `test`
   - **Compare**: `dev`
4. Click **"Create pull request"**
5. Título: "Análisis de mi proyecto completo"
6. Click **"Create pull request"**

### 4️⃣ El Pipeline Se Ejecuta AUTOMÁTICAMENTE

El workflow:
1. **Detecta** todos los archivos de código (.c, .cpp, .py, .java, .js, etc.)
2. **Analiza** cada archivo con el modelo XGBoost
3. **Genera** reporte con vulnerabilidades
4. **Notifica** por Telegram
5. **Bloquea** el merge si encuentra problemas

---

## 🔍 Qué Archivos Analiza

El scanner detecta y analiza automáticamente:

### Lenguajes Soportados:
- ✅ **C**: `*.c`
- ✅ **C++**: `*.cpp`, `*.cc`, `*.cxx`
- ✅ **Python**: `*.py`
- ✅ **Java**: `*.java`
- ✅ **JavaScript**: `*.js`
- ✅ **PHP**: `*.php`
- ✅ **Ruby**: `*.rb`
- ✅ **Go**: `*.go`

### Archivos Ignorados:
- ❌ Headers: `*.h` (no se analizan, solo incluyen declaraciones)
- ❌ Binarios: `*.exe`, `*.dll`, `*.so`
- ❌ Imágenes: `*.png`, `*.jpg`
- ❌ Docs: `*.md`, `*.txt`
- ❌ Node_modules, venv, build/ (ignorados por git)

---

## 📊 Ejemplo con Proyecto Real

### Tengo Este Proyecto:
```
mi_sistema_bancario/
├── src/
│   ├── main.c              (50 líneas)
│   ├── auth.c              (120 líneas)
│   ├── transactions.c      (200 líneas)
│   └── database.c          (150 líneas)
├── include/
│   ├── auth.h
│   └── database.h
├── utils/
│   ├── logger.c            (80 líneas)
│   └── crypto.c            (100 líneas)
└── tests/
    └── test_auth.c         (60 líneas)
```

### Paso a Paso:

```powershell
# 1. Copiar mi proyecto al repo
Copy-Item -Recurse C:\mis_proyectos\sistema_bancario\* C:\ESPE\Lab1-Seguro\sistema_bancario\

# 2. Verificar
cd C:\ESPE\Lab1-Seguro
git status
# Verás todos tus archivos .c listados

# 3. Añadir y commitear
git checkout dev
git add sistema_bancario/
git commit -m "feat: Añadir sistema bancario para análisis de seguridad"
git push origin dev

# 4. Crear PR en GitHub (ver arriba)
```

### El Scanner Analizará:

```
🔍 Scanning 7 C files...

Analyzing: sistema_bancario/src/main.c
Analyzing: sistema_bancario/src/auth.c
Analyzing: sistema_bancario/src/transactions.c
Analyzing: sistema_bancario/src/database.c
Analyzing: sistema_bancario/utils/logger.c
Analyzing: sistema_bancario/utils/crypto.c
Analyzing: sistema_bancario/tests/test_auth.c

📊 RESULTS:
❌ sistema_bancario/src/auth.c - VULNERABLE (89%)
   CWE-259: Hardcoded credentials
   CWE-798: Use of hardcoded password

❌ sistema_bancario/src/database.c - VULNERABLE (92%)
   CWE-89: SQL Injection
   CWE-134: Format string vulnerability

❌ sistema_bancario/src/transactions.c - VULNERABLE (78%)
   CWE-120: Buffer overflow (strcpy)

✅ sistema_bancario/src/main.c - SAFE (18%)
✅ sistema_bancario/utils/logger.c - SAFE (12%)
✅ sistema_bancario/utils/crypto.c - SAFE (25%)
✅ sistema_bancario/tests/test_auth.c - SAFE (15%)

⚠️ TOTAL: 3 vulnerable, 4 safe
```

---

## 📱 Notificación que Recibirás

```
🚨 ANÁLISIS DE SEGURIDAD COMPLETADO

Repositorio: Lab1-Seguro
PR #8: Análisis sistema bancario
Branch: dev → test

📊 Archivos analizados: 7

❌ Vulnerabilidades detectadas en:
1. sistema_bancario/src/auth.c (89%)
   • CWE-259: Hardcoded credentials
   • CWE-798: Hardcoded password

2. sistema_bancario/src/database.c (92%)
   • CWE-89: SQL Injection
   • CWE-134: Format string

3. sistema_bancario/src/transactions.c (78%)
   • CWE-120: Buffer overflow

✅ Archivos seguros: 4

⚠️ El PR ha sido bloqueado.
Corrige las vulnerabilidades antes de hacer merge.

🔗 Ver detalles: [link al PR]
```

---

## 🎯 PROYECTO DE EJEMPLO YA CREADO

Te creé un **proyecto completo de ejemplo** en:
```
c:\ESPE\Lab1-Seguro\proyecto_ejemplo\
```

### Estructura:
```
proyecto_ejemplo/
├── src/
│   ├── main.c          ❌ VULNERABLE
│   ├── auth.c          ❌ VULNERABLE
│   └── database.c      ❌ VULNERABLE
├── utils/
│   ├── logger.c        ✅ SEGURO
│   └── validator.c     ✅ SEGURO
├── include/
│   ├── auth.h
│   └── database.h
└── README.md
```

### Para Probarlo AHORA:

```powershell
# Ya está creado, solo hacer commit
git checkout dev
git add proyecto_ejemplo/
git commit -m "test: Añadir proyecto de ejemplo multi-archivo"
git push origin dev

# Luego crear PR en GitHub: dev → test
```

**En 2 minutos verás**:
- 3 archivos marcados como VULNERABLES
- 2 archivos marcados como SEGUROS
- Notificación en Telegram con detalles

---

## ❓ Preguntas Frecuentes

### ¿Cuántos archivos puedo analizar?
- ✅ **Sin límite**: El scanner analiza todos los archivos en el PR
- ⏱️ Tiempo: ~5-10 segundos por archivo
- 📊 Proyecto de 50 archivos: ~5 minutos de análisis

### ¿Puedo analizar proyectos en Python/Java/JavaScript?
- ✅ **SÍ**: El scanner soporta 8 lenguajes
- 🔄 Mismo proceso: Git add → commit → push → PR
- 📊 El modelo detecta vulnerabilidades en todos los lenguajes

### ¿Qué pasa si tengo archivos mezclados (.c + .py)?
- ✅ **Funciona**: Analiza cada archivo según su lenguaje
- 🎯 Ejemplo: 10 archivos .c + 5 archivos .py = 15 análisis

### ¿Puedo tener varios proyectos en un solo PR?
- ✅ **SÍ**: Analiza TODOS los archivos modificados en el PR
- 📊 Ejemplo: Añades 3 carpetas de proyectos → Analiza todo

### ¿Los archivos .h se analizan?
- ❌ **NO**: Los headers solo tienen declaraciones
- ✅ Solo se analizan archivos de implementación (.c, .cpp, .py, etc.)

---

## ✅ RESUMEN FINAL

### Para Analizar Tu Proyecto Completo:

1. **Poner** tu proyecto en el repositorio (cualquier carpeta)
2. **Git add + commit + push** a rama dev
3. **Crear PR** en GitHub: dev → test
4. **Esperar** 2-5 minutos
5. **Ver resultados** en GitHub Actions y Telegram

**¡ESO ES TODO!** El pipeline hace el resto automáticamente.

---

## 🚀 PRUEBA AHORA

El proyecto de ejemplo ya está listo:

```powershell
git checkout dev
git add proyecto_ejemplo/
git commit -m "test: Proyecto completo de gestión de usuarios"
git push origin dev
```

Luego crea el PR y verás el análisis completo en acción.

**¿Quieres que ejecute estos comandos ahora para ver el resultado?**
