# 🚀 CREAR PULL REQUEST - Guía Visual Paso a Paso

## ✅ OPCIÓN RÁPIDA - Sigue estos pasos:

### Paso 1: Abrir la página de GitHub
Ve a esta URL (ya la abrí en tu navegador):
```
https://github.com/CarlosCampoverde/Lab1-Seguro/compare/test...dev
```

O navega manualmente:
1. Ve a: https://github.com/CarlosCampoverde/Lab1-Seguro
2. Click en la pestaña **"Pull requests"**
3. Click en el botón verde **"New pull request"**

---

### Paso 2: Configurar las ramas

En la página de comparación, asegúrate de ver:

```
base: test  ←  compare: dev
```

Si ves otras ramas, cámbialas usando los menús desplegables:
- **base repository**: CarlosCampoverde/Lab1-Seguro
- **base**: `test` (la rama destino)
- **head repository**: CarlosCampoverde/Lab1-Seguro  
- **compare**: `dev` (tu rama con los cambios)

---

### Paso 3: Ver los cambios

Deberías ver algo como:
```
✅ Able to merge. These branches can be automatically merged.

Showing 15 changed files with 1,793 additions and 1 deletion.

proyecto_ejemplo/src/main.c
proyecto_ejemplo/src/auth.c
proyecto_ejemplo/src/database.c
proyecto_ejemplo/utils/logger.c
proyecto_ejemplo/utils/validator.c
ejemplo_para_probar.c
ejemplo_seguro.c
...
```

---

### Paso 4: Click en "Create pull request"

Verás un botón verde grande que dice:
```
[Create pull request]
```

**Click en ese botón**

---

### Paso 5: Completar el formulario

Se abrirá un formulario con dos campos:

#### Campo 1: Título
Copia y pega esto:
```
Test: Análisis de proyecto completo multi-archivo
```

#### Campo 2: Descripción (Leave a comment)
Copia y pega esto:
```
## 📦 Proyecto de Ejemplo para Testing

Este PR incluye un proyecto completo de gestión de usuarios para demostrar el análisis del pipeline.

### Archivos incluidos:
- ✅ **proyecto_ejemplo/**: Proyecto multi-archivo (9 archivos)
  - 3 archivos VULNERABLES
  - 2 archivos SEGUROS
  - Headers y documentación

### Vulnerabilidades esperadas:
- ❌ **Buffer overflow**: gets(), strcpy()
- ❌ **SQL injection**: sprintf() con input de usuario
- ❌ **Command injection**: system() sin sanitización
- ❌ **Hardcoded passwords**: Contraseñas en código
- ❌ **Format string**: printf() vulnerable

### Resultado esperado:
⚠️ Este PR debe ser **BLOQUEADO** por el scanner de seguridad.

El pipeline debe detectar al menos **4 archivos vulnerables**.
```

---

### Paso 6: Click en "Create pull request" (el segundo botón)

Abajo del formulario verás otro botón verde:
```
[Create pull request]
```

**Click en ese botón**

---

## ✅ ¡LISTO!

Después de crear el PR:

### 1️⃣ Verás la página del PR
Con URL como: `https://github.com/CarlosCampoverde/Lab1-Seguro/pull/X`

### 2️⃣ El workflow se ejecutará automáticamente
Verás en la parte de abajo:
```
⏳ Some checks haven't completed yet
   security-scan — In progress
   tests — Queued
```

### 3️⃣ Espera 2-3 minutos
El pipeline:
- Analizará los 5 archivos .c
- Detectará vulnerabilidades
- Enviará notificación a Telegram
- Bloqueará el PR

### 4️⃣ Verás el resultado
```
❌ security-scan — Failed
   Vulnerabilities detected in 4 file(s)
   
❌ Required checks failed
```

---

## 📸 CAPTURAS IMPORTANTES

Mientras esperas, toma screenshots de:

1. **PR recién creado** (con título y descripción)
2. **Checks en progreso** (security-scan running)
3. **Pestaña "Actions"**: https://github.com/CarlosCampoverde/Lab1-Seguro/actions
4. **Logs del scanner** (click en "security-scan" para ver detalles)
5. **Notificación en Telegram**
6. **PR bloqueado** (checks failed en rojo)

---

## 🎯 PRÓXIMOS PASOS

Una vez que el PR esté creado y el workflow termine:

1. ✅ Tomar screenshots
2. ✅ Verificar que detectó las 4 vulnerabilidades
3. ✅ Configurar branch protection
4. ✅ Hacer reporte LaTeX

---

## ❓ ¿Problemas?

### No veo el botón "Create pull request"
- Verifica que estás en: https://github.com/CarlosCampoverde/Lab1-Seguro/compare/test...dev
- Asegúrate de estar logueado en GitHub
- Verifica que las ramas son: base=test, compare=dev

### El botón está deshabilitado
- Puede que no haya cambios entre las ramas
- Verifica que hiciste git push origin dev

### No tengo permisos
- Asegúrate de estar logueado con la cuenta CarlosCampoverde
- Verifica que es tu repositorio

---

**¿Necesitas ayuda? Dime en qué paso estás.**
