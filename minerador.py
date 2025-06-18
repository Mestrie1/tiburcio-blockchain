import json
import time
import hashlib

BLOCKCHAIN_FILE = "blockchain.json"
TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"

RECOMPENSA_INICIAL = 50
INTERVALO_HALVING = 210000  # Ajuste conforme desejar
SUPPLY_MAXIMO = 21000000  # Total máximo de tokens a serem minerados

DIFICULDADE = 4  # Ajuste para mineração mais fácil ou difícil

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

def calcular_recompensa(indice_bloco):
    halvings = indice_bloco // INTERVALO_HALVING
    recompensa = RECOMPENSA_INICIAL // (2 ** halvings)
    if recompensa < 1:
        recompensa = 1  # recompensa mínima
    return recompensa

def calcular_total_minerado(blockchain):
    total = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx["de"] == "RECOMPENSA":
                total += tx["quantidade"]
    return total

def minerar_bloco(endereco_minerador):
    blockchain = carregar_blockchain()
    transacoes_pendentes = carregar_transacoes_pendentes()

    ultimo_bloco = blockchain[-1]
    novo_indice = ultimo_bloco["indice"] + 1

    total_minerado = calcular_total_minerado(blockchain)
    recompensa_atual = calcular_recompensa(novo_indice)

    if total_minerado + recompensa_atual > SUPPLY_MAXIMO:
        recompensa_atual = SUPPLY_MAXIMO - total_minerado
        if recompensa_atual <= 0:
            print("💰 Supply máximo alcançado! Não há mais recompensas.")
            recompensa_atual = 0

    if recompensa_atual > 0:
        transacoes_pendentes.append({
            "de": "RECOMPENSA",
            "para": endereco_minerador,
            "quantidade": recompensa_atual
        })

    novo_bloco = criar_bloco(transacoes_pendentes, ultimo_bloco["hash"], novo_indice)
    blockchain.append(novo_bloco)
    salvar_blockchain(blockchain)
    salvar_transacoes_pendentes([])

    print(f"✅ Bloco {novo_indice} minerado com sucesso! Recompensa: {recompensa_atual} tokens. Hash: {novo_bloco['hash']}")

if __name__ == "__main__":
    endereco = input("Digite seu endereço para receber as recompensas: ").strip()
    while True:
        minerar_bloco(endereco)
        
