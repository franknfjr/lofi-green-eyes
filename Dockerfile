# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Adicionar repositório não-livre para codecs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common && \
    apt-add-repository non-free && \
    apt-get update

# Instalar ffmpeg e suas dependências
RUN apt-get install -y --no-install-recommends \
    ffmpeg \
    libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*

# Configurar variável de ambiente para tokenizers
ENV TOKENIZERS_PARALLELISM=false

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
