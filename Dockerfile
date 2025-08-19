FROM python:3.10-slim

# Evitar mensajes interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements si lo tienes
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Instalar insightface (se recomienda especificar versión estable)
RUN pip install insightface==0.7.3 onnxruntime

# Copiar el código del proyecto
COPY . .

# Comando por defecto (ajústalo a tu script principal)
CMD ["python", "run.py"]
