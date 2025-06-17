import json
import hashlib
import time
import threading
from flask import Flask

app = Flask(__name__)

# Configurações iniciais
blockchain_file = "blockchain.json"
carteira_destino = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
recompensa = 50
dificuldade = 4  # Pode aumentar depois para dificultar mais a mineração

# Função para carregar ou criar a blockchain
def carregar_blockchain():
    try:
        with open(blockchain_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        bloco_genesis = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "previous_hash": "0",
            "nonce": 0,
            "hash": "0"
        }
        with open(blockchain_file, "w") as f:
            json.dump([bloco_genesis], f, indent=4)
        return [bloco_genesis]

# Função para salvar blockchain
def salvar_blockchain(blockchain):
    with open(blockchain_file, "w") as f:
        json.dump(blockchain, f, indent=4)

# Função de prova de trabalho
def prova_de_trabalho(bloco, dificuldade):
    prefixo = "0" * dificuldade
    while True:
        bloco["nonce"] += 1
        bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
        hash_bloco = hashlib.sha256(bloco_serializado).hexdigest()
        if hash_bloco.startswith(prefixo):
            bloco["hash"] = hash_bloco
            return bloco

# Função de mineração
def minerar():
    blockchain = carregar_blockchain()
    while True:
        ultimo_bloco = blockchain[-1]
        novo_bloco = {
            "index": ultimo_bloco["index"] + 1,
            "timestamp": time.time(),
            "transactions": [{"to": carteira_destino, "amount": recompensa}],
            "previous_hash": ultimo_bloco["hash"],
            "nonce": 0,
            "hash": ""
        }
        bloco_validado = prova_de_trabalho(novo_bloco, dificuldade)
        blockchain.append(bloco_validado)
        salvar_blockchain(blockchain)
        print(f"💎 Bloco {bloco_validado['index']} minerado! Recompensa: {recompensa} TiBúrcio")

# Rota web para ver status
@app.route("/")
def home():
    return "Minerador Tibúrcio rodando. Blocos minerados são salvos em blockchain.json."

# Iniciar o minerador em paralelo com o servidor Flask
if __name__ == "__main__":
    t = threading.Thread(target=minerar)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=10000)
