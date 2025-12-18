# Dockerfile para despliegue en Render/Railway
FROM python:3.11-slim

# Metadata
LABEL maintainer="equipo@espe.edu.ec"
LABEL description="Vulnerability Scanner API con XGBoost"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Crear usuario no-root
RUN useradd -m -u 1000 scanner && \
    mkdir -p /app && \
    chown -R scanner:scanner /app

WORKDIR /app

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard]

# Copiar código y modelos
COPY --chown=scanner:scanner . .

# Cambiar a usuario no-root
USER scanner

# Exponer puerto
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Comando de inicio
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
