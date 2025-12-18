# 🛡️ Pipeline CI/CD - Detección de Vulnerabilidades

## 📋 Descripción

Pipeline automatizado de seguridad que integra un modelo de Machine Learning (XGBoost) entrenado con metodología SEMMA para detectar vulnerabilidades en código **multi-lenguaje** (C, C++, Python, Java, JavaScript, PHP, Ruby, Go) dentro del flujo de trabajo GitHub Actions.

## 🎯 Características

- ✅ **Soporte multi-lenguaje**: 8 lenguajes (C, C++, Python, Java, JavaScript, PHP, Ruby, Go)
- ✅ **Análisis automático** en cada push y pull request
- ✅ **Detección de vulnerabilidades** con modelo XGBoost (65.5% accuracy en dataset balanceado)
- ✅ **Detección automática de lenguaje** basada en extensiones y patrones de código
- ✅ **Reportes HTML** con explicaciones SHAP interpretables
- ✅ **Alertas automáticas** mediante issues de GitHub
- ✅ **Comentarios en PRs** con resultados del análisis
- ✅ **Umbral de seguridad** configurable (70% por defecto)
- ✅ **Estadísticas por lenguaje** en reportes

## 🚀 Configuración

### 1. Prerequisitos

Asegúrate de tener los modelos entrenados:
- `xgboost_vulnerabilidades.pkl`
- `tfidf_vectorizer.pkl`

Estos se generan ejecutando el notebook `Lab1_SEMMA_Software_Seguro.ipynb`.

### 2. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 3. Estructura del proyecto

```
Lab1-Seguro/
├── .github/
│   └── workflows/
│       └── security-check.yml          # GitHub Actions workflow
├── predict_vulnerabilities.py          # Script de inferencia
├── generate_report.py                  # Generador de reportes HTML
├── requirements.txt                    # Dependencias Python
├── xgboost_vulnerabilidades.pkl        # Modelo entrenado
├── tfidf_vectorizer.pkl                # Vectorizador TF-IDF
└── Lab1_SEMMA_Software_Seguro.ipynb    # Notebook de entrenamiento
```

## 📊 Uso

### Análisis local

Analizar un archivo específico (cualquier lenguaje soportado):
```bash
python predict_vulnerabilities.py archivo.c
python predict_vulnerabilities.py script.py
python predict_vulnerabilities.py Main.java
python predict_vulnerabilities.py app.js
python predict_vulnerabilities.py index.php
```

Analizar un directorio completo:
```bash
python predict_vulnerabilities.py ./src
```

Generar reporte HTML:
```bash
python generate_report.py
```

### Pipeline CI/CD

El workflow se ejecuta automáticamente en:
- **Push** a las ramas: `main`, `dev`, `develop`
- **Pull Requests** hacia `main`

#### Funcionamiento del pipeline:

1. **Checkout del código**
2. **Instalación de dependencias**
3. **Verificación de modelos**
4. **Escaneo de archivos multi-lenguaje** (C, C++, Python, Java, JavaScript, TypeScript, PHP, Ruby, Go)
5. **Generación de reporte HTML** con explicaciones SHAP
6. **Comentario en PR** con resultados
7. **Creación de issue** si se detectan vulnerabilidades (solo en push)
8. **Fallo del workflow** si hay vulnerabilidades críticas (>70%)

## 📈 Modelo de Machine Learning

### Características del modelo

- **Algoritmo:** XGBoost (Gradient Boosting)
- **Metodología:** SEMMA (Sample, Explore, Modify, Model, Assess)
- **Dataset:** DiverseVul (10,000 funciones de 8 lenguajes)
- **Lenguajes:** C, C++, Python, Java, JavaScript, PHP, Ruby, Go
- **Accuracy:** ~65.5% (dataset balanceado)
- **Features:** 9 manuales (adaptadas por lenguaje) + 100 TF-IDF

### Features extraídas

**Manuales (adaptadas por lenguaje):**
- Longitud del código
- Número de líneas
- Funciones peligrosas detectadas (específicas por lenguaje):
  - C/C++: `strcpy`, `gets`, `system`
  - Python: `eval`, `exec`, `pickle.loads`
  - Java: `Runtime.exec`, `ProcessBuilder`
  - JavaScript: `eval`, `innerHTML`
  - PHP: `eval`, `exec`, `unserialize`
  - Ruby: `eval`, `system`, `Marshal.load`
  - Go: `exec.Command`, `unsafe.Pointer`
- Presencia de sanitización
- Complejidad ciclomática (adaptada por sintaxis)
- Anidamiento (llaves vs indentación)

**TF-IDF:**
- 100 features textuales con tri-gramas
- Capturan patrones sintácticos del código

## 🔍 Interpretabilidad con SHAP

El reporte HTML incluye gráficos SHAP que explican:
- ✅ Qué características del código influyen en la predicción
- ✅ Dirección del impacto (aumenta/disminuye riesgo)
- ✅ Magnitud de la contribución

Ejemplo de interpretación:
- **Rojo:** Features que aumentan probabilidad de vulnerabilidad
- **Azul:** Features que disminuyen probabilidad de vulnerabilidad

## 🎨 Reporte HTML

El reporte generado incluye:

- **Resumen ejecutivo** con estadísticas
- **Análisis detallado** de cada archivo
- **Barras de probabilidad** visuales
- **Gráficos SHAP** para archivos vulnerables
- **Metadata** (líneas, funciones peligrosas, confianza)

Descarga el artifact `vulnerability-report` desde la pestaña Actions de GitHub.

## ⚙️ Configuración avanzada

### Cambiar umbral de alerta

Edita `predict_vulnerabilities.py`:
```python
threshold = 0.7  # Cambia a 0.5, 0.8, etc.
```

### Modificar funciones peligrosas

Edita la lista `DANGEROUS_FUNCTIONS` en ambos scripts:
```python
DANGEROUS_FUNCTIONS = [
    'strcpy', 'gets', 'sprintf', 'strcat', 'scanf', 
    'system', 'exec', 'popen', 'memset', 'memcpy',
    # Agrega más funciones aquí
]
```

### Personalizar workflow

Edita `.github/workflows/security-check.yml`:
- Cambia ramas monitoreadas
- Ajusta permisos
- Modifica mensajes de alerta

## 🔒 Seguridad y permisos

El workflow requiere:
```yaml
permissions:
  contents: read      # Leer código
  issues: write       # Crear issues
  pull-requests: write # Comentar en PRs
```

## 📚 Metodología SEMMA

1. **Sample:** Muestreo balanceado de DiverseVul
2. **Explore:** Análisis exploratorio de vulnerabilidades
3. **Modify:** Feature engineering (manual + TF-IDF)
4. **Model:** Entrenamiento de XGBoost
5. **Assess:** Evaluación con métricas y SHAP

## 🐛 Troubleshooting

### Error: "Modelo no encontrado"
```bash
# Ejecuta el notebook primero
jupyter notebook Lab1_SEMMA_Software_Seguro.ipynb
```

### Error: "No se encontraron archivos C/C++"
El pipeline solo analiza archivos `.c`, `.cpp`, `.h`. Asegúrate de tenerlos en el repositorio.

### Workflow no se ejecuta
Verifica:
- Permisos de GitHub Actions habilitados
- El archivo está en `.github/workflows/`
- La rama está en la lista de triggers

## 📞 Soporte

Para problemas o mejoras, crea un issue en el repositorio.

---

**Desarrollado con ❤️ para el Laboratorio de Software Seguro - ESPE**
