from flask import Flask, jsonify
import json
import os

app = Flask(__name__)
CAMINHO_BLOCKCHAIN = "blockchain.json"

def calcular_saldo(endereco):
    saldo = 0
    if not os.path.exists(CAMINHO_BLOCKCHAIN):
        return saldo

    with open(CAMINHO_BLOCKCHAIN, "r") as f:
        try:
            blockchain = json.load(f)
        except json.JSONDecodeError:
            return saldo

    for bloco in blockchain:
        transacoes = bloco.get("transacoes", [])
        for tx in transacoes:
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
