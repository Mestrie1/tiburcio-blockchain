# Dockerfile para Tibúrcio Blockchain P2P
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt || true

EXPOSE 5000

CMD ["python3", "p2p_server.py"]
