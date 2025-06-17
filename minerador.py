from flask import Flask
import threading
import time
import json
import os

app = Flask(__name__)

ENDERECO_CARTEIRA = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
BLOCKCHAIN_FILE = "blockchain.json"
RECOMPENSA_MINERACAO = 10
DIFICULDADE = 5

# Função para carregar blockchain do arquivo
def carregar_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

# Função para salvar blockchain no arquivo
def salvar_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=4)

# Função para minerar um novo bloco com recompensa
def minerar():
    blockchain = carregar_blockchain()
    indice = len(blockchain)
    
    novo_bloco = {
        "indice": indice,
        "timestamp": time.time(),
        "transacoes": [
            {
                "remetente": "RECOMPENSA",
                "destinatario": ENDERECO_CARTEIRA,
                "quantidade": RECOMPENSA_MINERACAO
            }
        ],
        "hash_anterior": blockchain[-1]["hash"] if blockchain else "0"*64,
        "nonce": 0,
        "hash": ""
    }
    
    prefixo = "0" * DIFICULDADE
    while True:
        conteudo = f"{novo_bloco['indice']}{novo_bloco['timestamp']}{novo_bloco['transacoes']}{novo_bloco['hash_anterior']}{novo_bloco['nonce']}"
        novo_bloco["hash"] = str(abs(hash(conteudo)))
        if novo_bloco["hash"].startswith(prefixo):
            break
        novo_bloco["nonce"] += 1

    blockchain.append(novo_bloco)
    salvar_blockchain(blockchain)
    print(f"✅ Bloco {indice} minerado! Recompensa de {RECOMPENSA_MINERACAO} TiBúrcio enviada para {ENDERECO_CARTEIRA}")

# Loop contínuo de mineração
def loop_mineracao():
    while True:
        minerar()

@app.route("/")
def home():
    return "✅ Minerador Tibúrcio rodando e salvando recompensas!"

if __name__ == "__main__":
    threading.Thread(target=loop_mineracao, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
