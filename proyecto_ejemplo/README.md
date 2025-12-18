# 🏢 Proyecto de Ejemplo - Sistema de Gestión de Usuarios

Este es un **proyecto completo multi-archivo** para demostrar cómo el pipeline analiza proyectos enteros.

## 📁 Estructura del Proyecto

```
proyecto_ejemplo/
├── src/
│   ├── main.c              (VULNERABLE - Punto de entrada)
│   ├── auth.c              (VULNERABLE - Autenticación insegura)
│   └── database.c          (VULNERABLE - SQL injection)
├── include/
│   ├── auth.h              (Headers)
│   └── database.h
├── utils/
│   ├── logger.c            (SEGURO)
│   └── validator.c         (SEGURO - Validación correcta)
└── README.md
```

## 🔍 Qué Detectará el Scanner

### ❌ Archivos VULNERABLES:
- **main.c**: Buffer overflow, gets(), strcpy()
- **auth.c**: Passwords en plain text, command injection
- **database.c**: SQL injection, sprintf()

### ✅ Archivos SEGUROS:
- **logger.c**: Uso correcto de fgets(), snprintf()
- **validator.c**: Input validation, sanitización

## 🚀 Cómo Analizar Este Proyecto

```bash
# 1. Añadir todo el proyecto
git add proyecto_ejemplo/

# 2. Commit
git commit -m "feat: Añadir proyecto completo de gestión"

# 3. Push
git push origin dev

# 4. Crear PR en GitHub: dev → test
```

**El scanner analizará TODOS los archivos .c automáticamente**

## 📊 Resultado Esperado

```
🔍 Scanning 5 C files...

❌ src/main.c - VULNERABLE (95% probability)
   - CWE-120: Buffer overflow (gets, strcpy)
   - CWE-78: Command injection (system)

❌ src/auth.c - VULNERABLE (88% probability)
   - CWE-259: Hardcoded password
   - CWE-78: Command injection

❌ src/database.c - VULNERABLE (92% probability)
   - CWE-89: SQL injection
   - CWE-134: Format string (sprintf)

✅ utils/logger.c - SAFE (15% probability)
✅ utils/validator.c - SAFE (12% probability)

⚠️ TOTAL: 3 archivos vulnerables de 5
```

## 📱 Notificación Telegram

Recibirás:
```
🚨 ALERTA DE SEGURIDAD

Proyecto: proyecto_ejemplo/
3 archivos vulnerables detectados:

❌ src/main.c (95%)
❌ src/auth.c (88%)
❌ src/database.c (92%)

El PR ha sido bloqueado.
Corrige las vulnerabilidades antes de hacer merge.
```
