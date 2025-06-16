FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask

CMD ["python3", "p2p_server.py"]
