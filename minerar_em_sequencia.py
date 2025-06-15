import json
import time
import hashlib

# Configurações da blockchain
MAX_TIBURCIO = 21_000_000
RECOMPENSA_INICIAL = 50
HALVING_INTERVAL = 210_000

# Parâmetros da dificuldade
DIFICULDADE_INICIAL = 4  # número de zeros iniciais no hash (ajusta o "alvo")
AJUSTE_DIFICULDADE_INTERVALO = 10  # blocos para ajustar dificuldade
TEMPO_ALVO_BLOCO = 20  # segundos alvo por bloco (pra teste rápido)

def carregar_blockchain():
    try:
        with open("blockchain.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def salvar_blockchain(blockchain):
    with open("blockchain.json", "w") as arquivo:
        json.dump(blockchain, arquivo, indent=4)

def calcular_recompensa(altura_bloco):
    halvings = altura_bloco // HALVING_INTERVAL
    recompensa = RECOMPENSA_INICIAL >> halvings
    return max(recompensa, 0)

def calcular_hash(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

def proof_of_work(bloco, dificuldade):
    prefixo = "0" * dificuldade
    nonce = 0
    while True:
        bloco['nonce'] = nonce
        hash_atual = calcular_hash(bloco)
        if hash_atual.startswith(prefixo):
            return hash_atual, nonce
        nonce += 1

def ajustar_dificuldade(blockchain):
    altura = len(blockchain)
    if altura == 0 or altura % AJUSTE_DIFICULDADE_INTERVALO != 0:
        # Mantém dificuldade do último bloco ou inicial
        return blockchain[-1]['dificuldade'] if blockchain else DIFICULDADE_INICIAL

    bloco_anterior = blockchain[-AJUSTE_DIFICULDADE_INTERVALO]
    bloco_atual = blockchain[-1]

    tempo_real = bloco_atual['timestamp'] - bloco_anterior['timestamp']
    tempo_esperado = AJUSTE_DIFICULDADE_INTERVALO * TEMPO_ALVO_BLOCO

    dificuldade_antiga = blockchain[-1]['dificuldade']
    if tempo_real < tempo_esperado / 2:
        return dificuldade_antiga + 1
    elif tempo_real > tempo_esperado * 2 and dificuldade_antiga > 1:
        return dificuldade_antiga - 1
    else:
        return dificuldade_antiga

def minerar_bloco(index, anterior_hash, recompensa, minerador, dificuldade):
    bloco = {
        "index": index,
        "timestamp": time.time(),
        "transacoes": [],
        "recompensa": {
            "para": minerador,
            "quantidade": recompensa
        },
        "anterior": anterior_hash,
        "dificuldade": dificuldade,
        "nonce": 0  # vai ser atualizado no proof_of_work
    }
    hash_proof, nonce = proof_of_work(bloco, dificuldade)
    bloco['hash'] = hash_proof
    bloco['nonce'] = nonce
    return bloco

def minerar_em_sequencia(minerador, quantidade_blocos):
    blockchain = carregar_blockchain()

    for _ in range(quantidade_blocos):
        index = len(blockchain)
        altura_bloco = index

        total_emitido = sum(b["recompensa"]["quantidade"] for b in blockchain)
        recompensa = calcular_recompensa(altura_bloco)

        if total_emitido + recompensa > MAX_TIBURCIO:
            recompensa = max(0, MAX_TIBURCIO - total_emitido)

        if recompensa == 0:
            print("Limite máximo de TiBúrcio emitidos alcançado.")
            break

        anterior_hash = blockchain[-1]["hash"] if blockchain else "0" * 64
        dificuldade = ajustar_dificuldade(blockchain)

        print(f"Minerando bloco {index} com dificuldade {dificuldade}...")

        bloco = minerar_bloco(index, anterior_hash, recompensa, minerador, dificuldade)

        blockchain.append(bloco)
        salvar_blockchain(blockchain)

        print(f"Bloco {index} minerado! Recompensa: {recompensa} TiBúrcio para {minerador}")
        print(f"Hash: {bloco['hash']}")
        print(f"Nonce: {bloco['nonce']}")
        print("-" * 40)

if __name__ == "__main__":
    minerador = input("Endereço da carteira mineradora: ")
    quantidade_blocos = int(input("Quantidade de blocos para minerar: "))
    minerar_em_sequencia(minerador, quantidade_blocos)
