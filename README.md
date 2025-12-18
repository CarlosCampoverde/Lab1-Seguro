# 🔒 Pipeline CI/CD Seguro con IA para Detección de Vulnerabilidades

[![Security Scan](https://github.com/YOUR_USERNAME/Lab1-Seguro/workflows/Security%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/Lab1-Seguro/actions)
[![Deployment](https://img.shields.io/badge/deploy-Render-46E3B7)](https://your-app.onrender.com)
[![Model Accuracy](https://img.shields.io/badge/accuracy-71.34%25-yellow)](./Lab1_SEMMA_Software_Seguro.ipynb)

**Universidad de las Fuerzas Armadas ESPE**  
**Desarrollo de Software Seguro - Proyecto Final**  
**Docente:** Ing. Geovanny Cudco  
**Fecha:** 17 de diciembre de 2025

## 📋 Descripción

Pipeline CI/CD completamente automatizado que integra **Inteligencia Artificial basada en Minería de Datos** (XGBoost) para detectar vulnerabilidades en código fuente antes de llegar a producción.

**🚫 NO USA LLM** - Solo modelos de ML tradicional entrenados con datasets públicos.

## 🎯 Características del Pipeline

- ✅ **Detección automática de vulnerabilidades** con modelo XGBoost
- ✅ **8 lenguajes soportados**: C, C++, Python, Java, JavaScript, PHP, Ruby, Go
- ✅ **Flujo automatizado**: dev → test → main
- ✅ **Notificaciones Telegram** en todas las fases
- ✅ **Bloqueo automático** de código vulnerable
- ✅ **Despliegue automático** a producción (Render/Railway)
- ✅ **Branch protection** en test y main
- ✅ **Metodología SEMMA** completa aplicada

## Integrantes  
Carlos Campoverde, Juan Pasquel; Anthony Villareal

## Dataset utilizado  
**DiverseVul** (bstee615/diversevul – Hugging Face)  https://huggingface.co/datasets/bstee615/diversevul 
- **Lenguajes soportados:** 8 (C, C++, Python, Java, JavaScript, PHP, Ruby, Go) ✅
- **Total funciones originales:** 264.393  
- **Vulnerables reales:** 15.145  
- **Muestreo balanceado final:** 10.000 funciones (5.000 vulnerables + 5.000 seguras) → requisito punto 4.1 cumplido

## Metodología SEMMA aplicada  
| Fase     | Descripción cumplida                                                                 |
|----------|---------------------------------------------------------------------------------------|
| Sample   | Muestreo estratificado balanceado 50/50                                               |
| Explore  | Estadísticas descriptivas + 4 visualizaciones (boxplots, histogramas, countplot)     |
| Modify   | Feature engineering completo: <br>• TF-IDF (100 tokens) <br>• Funciones peligrosas por lenguaje (strcpy, eval, exec, etc.) <br>• Detección automática de lenguaje de programación <br>• Presencia de sanitización <br>• Complejidad ciclomática adaptada por lenguaje <br>• Anidamiento (llaves para C/Java, indentación para Python/Ruby) |
| Model    | XGBoost (scikit-learn + xgboost) – 500 árboles, profundidad 12                       |
| Assess   | **Accuracy 71.34%** - Modelo funcional para detección de vulnerabilidades <br>Classification report + matriz de confusión implementados <br>Coherente con complejidad del dataset multi-lenguaje |

## Resultados finales  

graph LR
    A[Bases de Datos<br/>Ficheros<br/>(e.g., DiverseVul Dataset)] --> B[Extracción<br/>(Sample/Explore: Tokens, AST, Diff PR)]
    B --> C[Transformación<br/>(Modify: TF-IDF, Features peligrosas,<br/>XGBoost Clasificación Vulnerable/Seguro)]
    C --> D[Carga<br/>(Model/Assess: Output a Pipeline CI/CD,<br/>Notificaciones Telegram)]
    D --> E[Bases de Datos/Ficheros<br/>(Issue/PR Rechazo o Merge a Test/Main,<br/>Despliegue Render)]
    E --> A  %% Ciclo para iteraciones
    style B fill:#E1F5FE
    style C fill:#FFF3E0
    style D fill:#F3E5F5
    style A fill:#E8F5E8
    style E fill:#FFF8E1