# scraper/Dockerfile
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies first
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY config.py .
COPY scrapers/ ./scrapers/
COPY models/ ./models/
COPY main_*.py .
COPY utils.py .

# Single entry point script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]