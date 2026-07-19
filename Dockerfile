FROM python:3.11-slim

# Install system dependencies
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

# Start Ollama server in background + pull models
RUN ollama serve & sleep 8 && \
    ollama pull moondream && \
    ollama pull llama3.2 && \
    pkill ollama

COPY . .

CMD ["python", "bot.py"]
