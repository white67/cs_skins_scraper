FROM python:3.12-slim
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .
COPY scrapers/ ./scrapers/
COPY models/ ./models/
COPY main_*.py .
COPY utils.py .

# single entry point script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]