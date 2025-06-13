ENDERECO_DESTINO = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
import hashlib
import json
import time
import os

ARQUIVO_BLOCKCHAIN = "blockchain.json"
DIFICULDADE = 4  # Quantidade de zeros no hash inicial (aumente para minerar mais devagar)
RECOMPENSA = 50
ENDERECO_DESTINO = "3uukRWcu1ZHhfPJCFiscYNMQmLYsHMuRHn3RfmUyWkcZ"  # SEU ENDEREÇO AQUI

def criar_bloco(indice, timestamp, transacoes, hash_anterior, nonce):
    bloco = {
        'indice': indice,
        'timestamp': timestamp,
        'transacoes': transacoes,
        'hash_anterior': hash_anterior,
        'nonce': nonce,
        'hash': calcular_hash(indice, timestamp, transacoes, hash_anterior, nonce)
    }
    return bloco

def calcular_hash(indice, timestamp, transacoes, hash_anterior, nonce):
    bloco_string = f"{indice}{timestamp}{transacoes}{hash_anterior}{nonce}"
    return hashlib.sha256(bloco_string.encode()).hexdigest()

def carregar_blockchain():
    if os.path.exists(ARQUIVO_BLOCKCHAIN):
        with open(ARQUIVO_BLOCKCHAIN, "r") as f:
            return json.load(f)
    else:
        bloco_genesis = criar_bloco(0, time.time(), [], "0", 0)
        with open(ARQUIVO_BLOCKCHAIN, "w") as f:
            json.dump([bloco_genesis], f, indent=4)
        return [bloco_genesis]

def salvar_blockchain(blockchain):
    with open(ARQUIVO_BLOCKCHAIN, "w") as f:
        json.dump(blockchain, f, indent=4)

def minerar_novo_bloco(blockchain, transacoes):
    ultimo_bloco = blockchain[-1]
    indice = ultimo_bloco["indice"] + 1
    timestamp = time.time()
    hash_anterior = ultimo_bloco["hash"]
    nonce = 0

    while True:
        hash_calculado = calcular_hash(indice, timestamp, transacoes, hash_anterior, nonce)
        if hash_calculado.startswith("0" * DIFICULDADE):
            novo_bloco = criar_bloco(indice, timestamp, transacoes, hash_anterior, nonce)
            blockchain.append(novo_bloco)
            salvar_blockchain(blockchain)
            print(f"✅ Bloco {indice} minerado: {hash_calculado}")
            return novo_bloco
        nonce += 1

def main():
    blockchain = carregar_blockchain()
    while True:
        transacoes = [{"origem": "recompensa", "destino": ENDERECO_DESTINO, "quantidade": RECOMPENSA}]
        minerar_novo_bloco(blockchain, transacoes)

if __name__ == "__main__":
    main()
