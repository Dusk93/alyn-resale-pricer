FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl zstd ca-certificates procps && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use a very reliable small model
CMD ollama serve & sleep 10 && ollama pull llava:7b && python bot.py
