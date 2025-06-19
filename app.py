from flask import Flask, request, jsonify
import json
import hashlib

app = Flask(__name__)

BLOCKCHAIN_FILE = "blockchain.json"
TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"

def carregar_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def calcular_saldo(endereco, blockchain):
    saldo = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx["de"] == endereco:
                saldo -= tx["quantidade"]
            if tx["para"] == endereco:
                saldo += tx["quantidade"]
    return saldo

@app.route('/nova_transacao', methods=['POST'])
def nova_transacao():
    tx = request.get_json()
    with open(TRANSACOES_PENDENTES_FILE, "r") as f:
        try:
            transacoes = json.load(f)
        except:
            transacoes = []
    transacoes.append(tx)
    with open(TRANSACOES_PENDENTES_FILE, "w") as f:
        json.dump(transacoes, f, indent=4)
    return jsonify({'status': 'Transação recebida'}), 201

@app.route('/novo_bloco', methods=['POST'])
def novo_bloco():
    bloco = request.get_json()
    blockchain = carregar_blockchain()
    blockchain.append(bloco)
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=4)
    with open(TRANSACOES_PENDENTES_FILE, "w") as f:
        json.dump([], f)  # limpa transações pendentes
    return jsonify({'status': 'Bloco adicionado'}), 201

@app.route('/transacoes_pendentes', methods=['GET'])
def transacoes_pendentes():
    with open(TRANSACOES_PENDENTES_FILE, "r") as f:
        try:
            transacoes = json.load(f)
        except:
            transacoes = []
    return jsonify(transacoes), 200

@app.route('/saldo/<endereco>', methods=['GET'])
def saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = calcular_saldo(endereco, blockchain)
    return jsonify({'endereco': endereco, 'saldo': saldo}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
