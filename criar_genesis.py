import json
import time
import hashlib

ARQUIVO_BLOCKCHAIN = "blockchain.json"

def calcular_hash_bloco(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

def criar_bloco_genesis():
    bloco_genesis = {
        "indice": 0,
        "timestamp": time.time(),
        "transacoes": [
            {
                "de": "RECOMPENSA",
                "para": "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM",
                "quantidade": 50
            }
        ],
        "anterior": "0" * 40,
        "nonce": 0,
        "hash": ""
    }

    dificuldade = 4
    prefixo = "0" * dificuldade
    nonce = 0
    while True:
        bloco_genesis["nonce"] = nonce
        hash_calculado = calcular_hash_bloco(bloco_genesis)
        if hash_calculado.startswith(prefixo):
            bloco_genesis["hash"] = hash_calculado
            break
        nonce += 1

    with open(ARQUIVO_BLOCKCHAIN, "w") as f:
        json.dump([bloco_genesis], f, indent=4)

    print("Bloco gênesis criado com sucesso!")
    print(f"Hash: {bloco_genesis['hash']}")

if __name__ == "__main__":
    criar_bloco_genesis()
