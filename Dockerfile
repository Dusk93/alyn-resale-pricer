FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl zstd ca-certificates procps && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pull model during build
RUN ollama serve & sleep 12 && \
    ollama pull moondream && \
    pkill ollama || true

COPY . .

CMD ["python", "bot.py"]
