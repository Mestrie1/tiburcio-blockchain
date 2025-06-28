from flask import Flask, jsonify
import os
import json

app = Flask(__name__)
PASTA_BLOCOS = "blocos"

def calcular_saldo(endereco):
    saldo = 0
    if not os.path.exists(PASTA_BLOCOS):
        return saldo

    for arquivo in os.listdir(PASTA_BLOCOS):
        caminho = os.path.join(PASTA_BLOCOS, arquivo)
        with open(caminho, "r") as f:
            bloco = json.load(f)
            for tx in bloco.get("transacoes", []):
                if tx.get("para") == endereco:
                    saldo += tx.get("quantidade", 0)
                if tx.get("de") == endereco:
                    saldo -= tx.get("quantidade", 0)
    return saldo

@app.route("/")
def index():
    return "Servidor Saldo Tibúrcio Blockchain rodando com saldos reais!"

@app.route("/saldo/<endereco>", methods=["GET"])
def saldo(endereco):
    saldo = calcular_saldo(endereco)
    return jsonify({"endereco": endereco, "saldo": saldo})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
