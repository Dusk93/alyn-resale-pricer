FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download small models
RUN ollama pull moondream
RUN ollama pull llama3.2

COPY . .

CMD ["python", "bot.py"]