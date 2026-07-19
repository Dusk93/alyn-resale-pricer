FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    ca-certificates \
    procps \               # Needed for pkill
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Start Ollama + pull small model only (moondream is much smaller)
RUN ollama serve & sleep 10 && \
    ollama pull moondream && \
    pkill ollama || true

COPY . .

CMD ["python", "bot.py"]
