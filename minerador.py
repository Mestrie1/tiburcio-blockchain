import json
import hashlib
import time
import os

RECOMPENSA_MINERACAO = 50
DIFICULDADE = 5
CARTEIRA_MINERADOR = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
ARQUIVO_BLOCKCHAIN = "blockchain.json"

def carregar_blockchain():
    if os.path.exists(ARQUIVO_BLOCKCHAIN):
        with open(ARQUIVO_BLOCKCHAIN, "r") as f:
            return json.load(f)
    return []

def salvar_blockchain(blockchain):
    with open(ARQUIVO_BLOCKCHAIN, "w") as f:
        json.dump(blockchain, f, indent=4)

def calcular_hash(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

def minerar_bloco(blockchain, carteira_destino):
    indice = len(blockchain)
    transacoes = [{"de": "RECOMPENSA", "para": carteira_destino, "quantidade": RECOMPENSA_MINERACAO}]
    bloco = {
        "indice": indice,
        "transacoes": transacoes,
        "anterior": blockchain[-1]["hash"] if blockchain else "0"*64,
        "nonce": 0,
        "timestamp": time.time()
    }

    prefixo_dificuldade = "0" * DIFICULDADE

    while True:
        bloco_hash = calcular_hash(bloco)
        if bloco_hash.startswith(prefixo_dificuldade):
            bloco["hash"] = bloco_hash
            return bloco
        else:
            bloco["nonce"] += 1

def minerar():
    blockchain = carregar_blockchain()
    while True:
        novo_bloco = minerar_bloco(blockchain, CARTEIRA_MINERADOR)
        blockchain.append(novo_bloco)
        salvar_blockchain(blockchain)
        print(f"💎 Bloco {novo_bloco['indice']} minerado! Recompensa: {RECOMPENSA_MINERACAO} TiBúrcio")
        time.sleep(1)

if __name__ == "__main__":
    minerar()
