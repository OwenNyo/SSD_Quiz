# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install git + flask
RUN apt-get update && apt-get install -y git && \
    pip install flask && \
    rm -rf /var/lib/apt/lists/*

COPY web /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
