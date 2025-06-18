import json
import time
import hashlib

BLOCKCHAIN_FILE = "blockchain.json"
TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"
RECOMPENSA_MINERADOR = 50  # Pode ajustar
DIFICULDADE = 4  # Pode ajustar para mineração mais difícil ou fácil

def carregar_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        bloco_genesis = {
            "indice": 0,
            "transacoes": [],
            "anterior": "0"*64,
            "nonce": 0,
            "timestamp": time.time(),
            "hash": ""
        }
        bloco_genesis["hash"] = calcular_hash(bloco_genesis)
        salvar_blockchain([bloco_genesis])
        return [bloco_genesis]

def salvar_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=4)

def carregar_transacoes_pendentes():
    try:
        with open(TRANSACOES_PENDENTES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_transacoes_pendentes(transacoes):
    with open(TRANSACOES_PENDENTES_FILE, "w") as f:
        json.dump(transacoes, f, indent=4)

def calcular_hash(bloco):
    bloco_copy = dict(bloco)
    bloco_copy.pop("hash", None)
    bloco_str = json.dumps(bloco_copy, sort_keys=True).encode()
    return hashlib.sha256(bloco_str).hexdigest()

def prova_de_trabalho(bloco):
    bloco["nonce"] = 0
    prefixo = "0" * DIFICULDADE
    while True:
        bloco["hash"] = calcular_hash(bloco)
        if bloco["hash"].startswith(prefixo):
            return bloco
        bloco["nonce"] += 1

def criar_bloco(transacoes, hash_anterior, indice):
    bloco = {
        "indice": indice,
        "transacoes": transacoes,
        "anterior": hash_anterior,
        "nonce": 0,
        "timestamp": time.time(),
        "hash": ""
    }
    bloco = prova_de_trabalho(bloco)
    return bloco

def minerar_bloco(endereco_minerador):
    blockchain = carregar_blockchain()
    transacoes_pendentes = carregar_transacoes_pendentes()

    transacoes_pendentes.append({
        "de": "RECOMPENSA",
        "para": endereco_minerador,
        "quantidade": RECOMPENSA_MINERADOR
    })

    ultimo_bloco = blockchain[-1]
    novo_indice = ultimo_bloco["indice"] + 1

    novo_bloco = criar_bloco(transacoes_pendentes, ultimo_bloco["hash"], novo_indice)

    blockchain.append(novo_bloco)
    salvar_blockchain(blockchain)

    salvar_transacoes_pendentes([])

    print(f"✅ Bloco {novo_indice} minerado com sucesso! Hash: {novo_bloco['hash']}")

if __name__ == "__main__":
    endereco = input("Digite seu endereço para receber as recompensas: ").strip()
    while True:
        minerar_bloco(endereco)
        time.sleep(1)  # Pequena pausa para evitar loop muito rápido
