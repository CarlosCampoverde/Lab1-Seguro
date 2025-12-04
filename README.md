# Laboratorio 1 - Desarrollo de Software Seguro  
**Universidad de las Fuerzas Armadas ESPE**  
**Carrera de Ingeniería en Software**  
**Docente:** Ing. Geovanny Cudco  
**Fecha:** 28 de noviembre de 2025  

## Título  
**Aplicación de Minería de Datos en el Desarrollo de Software Seguro usando metodología SEMMA**

## Integrantes  
Carlos Campoverde, Juan Pasquel; Anthony Villareal

## Dataset utilizado  
**DiverseVul** (bstee615/diversevul – Hugging Face)  https://huggingface.co/datasets/bstee615/diversevul 
- Total funciones originales: 264.393  
- Vulnerables reales: 15.145  
- Muestreo balanceado final: **10.000 funciones** (5.000 vulnerables + 5.000 seguras) → requisito punto 4.1 cumplido

## Metodología SEMMA aplicada  
| Fase     | Descripción cumplida                                                                 |
|----------|---------------------------------------------------------------------------------------|
| Sample   | Muestreo estratificado balanceado 50/50                                               |
| Explore  | Estadísticas descriptivas + 4 visualizaciones (boxplots, histogramas, countplot)     |
| Modify   | Feature engineering completo: <br>• TF-IDF (100 tokens) <br>• Funciones peligrosas (strcpy, gets, sprintf, system, etc.) <br>• Presencia de sanitización <br>• Complejidad ciclomática y anidamiento |
| Model    | XGBoost (scikit-learn + xgboost) – 500 árboles, profundidad 12                       |
| Assess   | Accuracy 65.5 % (coherente con baselines del paper original DiverseVul – RAID 2023) <br>Classification report + matriz de confusión + SHAP values |

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