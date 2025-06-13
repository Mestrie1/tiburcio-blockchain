import hashlib
import json
import time
import os

# CONFIGURAÇÃO — SEU ENDEREÇO DA CARTEIRA
MINERADOR_ENDERECO = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"

# CONFIGURAÇÃO DA RECOMPENSA POR BLOCO
RECOMPENSA = 50

# Função para calcular o hash de um bloco
def calcular_hash(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

# Função para carregar a blockchain
def carregar_blockchain():
    if os.path.exists("blockchain.json"):
        with open("blockchain.json", "r") as arquivo:
            return json.load(arquivo)
    return []

# Função para salvar a blockchain
def salvar_blockchain(blockchain):
    with open("blockchain.json", "w") as arquivo:
        json.dump(blockchain, arquivo, indent=4)

# Função para minerar um novo bloco
def minerar_bloco(blockchain, transacoes):
    ultimo_hash = blockchain[-1]["hash"] if blockchain else "0"
    index = len(blockchain) + 1
    timestamp = time.time()

    bloco = {
        "index": index,
        "timestamp": timestamp,
        "transacoes": transacoes,
        "recompensa": {
            "para": MINERADOR_ENDERECO,
            "quantidade": RECOMPENSA
        },
        "anterior": ultimo_hash,
        "nonce": 0
    }

    dificuldade = 4  # Número de zeros iniciais no hash (pode aumentar depois)
    prefixo_alvo = "0" * dificuldade

    while True:
        hash_bloco = calcular_hash(bloco)
        if hash_bloco.startswith(prefixo_alvo):
            bloco["hash"] = hash_bloco
            return bloco
        bloco["nonce"] += 1

# Função para carregar transações pendentes
def carregar_transacoes_pendentes():
    if os.path.exists("transacoes_pendentes.txt"):
        with open("transacoes_pendentes.txt", "r") as arquivo:
            return json.load(arquivo)
    return []

# Função para limpar as transações pendentes após mineração
def limpar_transacoes_pendentes():
    if os.path.exists("transacoes_pendentes.txt"):
        os.remove("transacoes_pendentes.txt")

# Loop principal de mineração
blockchain = carregar_blockchain()

while True:
    transacoes = carregar_transacoes_pendentes()
    bloco = minerar_bloco(blockchain, transacoes)
    blockchain.append(bloco)
    salvar_blockchain(blockchain)
    limpar_transacoes_pendentes()
    print(f"🪙 Bloco {bloco['index']} minerado! Hash: {bloco['hash']}")
    print(f"🏆 {RECOMPENSA} $Tib enviados para: {MINERADOR_ENDERECO}\n")
