FROM python:3.11-slim

# Install required system dependencies including zstd
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download small models (critical for free tier)
RUN ollama pull moondream
RUN ollama pull llama3.2

COPY . .

# Environment variables for Telegram bot
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

CMD ["python", "bot.py"]
