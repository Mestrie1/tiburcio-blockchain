import json
import time
import hashlib

MAX_TIBURCIO = 21_000_000
RECOMPENSA_INICIAL = 50
HALVING_INTERVAL = 210_000
AJUSTE_INTERVALO = 2016
TEMPO_OBJETIVO = 600  # 10 minutos por bloco, como no Bitcoin
dificuldade_inicial = 4
ARQUIVO_BLOCKCHAIN = "blockchain.json"

def calcular_hash(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

def criar_bloco_genese():
    bloco = {
        "index": 0,
        "timestamp": time.time(),
        "transacoes": [],
        "recompensa": {"para": "genesis", "quantidade": 0},
        "dificuldade": dificuldade_inicial,
        "nonce": 0,
        "anterior": "0" * 64,
    }
    bloco['hash'] = calcular_hash(bloco)
    return bloco

def carregar_blockchain():
    try:
        with open(ARQUIVO_BLOCKCHAIN, "r") as f:
            blockchain = json.load(f)
        return blockchain
    except FileNotFoundError:
        blockchain = [criar_bloco_genese()]
        salvar_blockchain(blockchain)
        return blockchain

def salvar_blockchain(blockchain):
    with open(ARQUIVO_BLOCKCHAIN, "w") as f:
        json.dump(blockchain, f, indent=4)

def calcular_saldo(endereco, blockchain):
    saldo = 0
    for bloco in blockchain:
        for tx in bloco['transacoes']:
            if tx.get('para') == endereco:
                saldo += tx.get('quantidade', 0)
            if tx.get('de') == endereco:
                saldo -= tx.get('quantidade', 0)
        recompensa = bloco.get('recompensa', {})
        if recompensa.get('para') == endereco:
            saldo += recompensa.get('quantidade', 0)
    return saldo

def hash_valido(hash_, dificuldade):
    return hash_.startswith("0" * dificuldade)

def ajustar_dificuldade(blockchain):
    ultimo_bloco = blockchain[-1]
    indice = ultimo_bloco['index']

    if indice % AJUSTE_INTERVALO != 0 or indice == 0:
        return ultimo_bloco.get('dificuldade', dificuldade_inicial)

    bloco_referencia = blockchain[indice - AJUSTE_INTERVALO]
    tempo_real = ultimo_bloco['timestamp'] - bloco_referencia['timestamp']
    tempo_ideal = AJUSTE_INTERVALO * TEMPO_OBJETIVO

    dificuldade_atual = ultimo_bloco.get('dificuldade', dificuldade_inicial)

    if tempo_real < tempo_ideal / 2:
        dificuldade_atual += 1
        print("Dificuldade aumentada para", dificuldade_atual)
    elif tempo_real > tempo_ideal * 2 and dificuldade_atual > 1:
        dificuldade_atual -= 1
        print("Dificuldade diminuída para", dificuldade_atual)
    else:
        print("Dificuldade mantida em", dificuldade_atual)

    return dificuldade_atual

def minerar_bloco(transacoes, endereco_minerador, blockchain):
    ultimo_bloco = blockchain[-1]
    index = ultimo_bloco['index'] + 1
    timestamp = time.time()
    dificuldade = ajustar_dificuldade(blockchain)

    recompensa = RECOMPENSA_INICIAL * (0.5 ** (index // HALVING_INTERVAL))

    bloco = {
        "index": index,
        "timestamp": timestamp,
        "transacoes": transacoes,
        "recompensa": {
            "para": endereco_minerador,
            "quantidade": recompensa
        },
        "dificuldade": dificuldade,
        "nonce": 0,
        "anterior": ultimo_bloco['hash'],
    }

    print(f"Minerando bloco {index} com dificuldade {dificuldade}...")

    nonce = 0
    while True:
        bloco['nonce'] = nonce
        hash_bloco = calcular_hash(bloco)
        if hash_valido(hash_bloco, dificuldade):
            bloco['hash'] = hash_bloco
            break
        nonce += 1

    blockchain.append(bloco)
    salvar_blockchain(blockchain)
    print(f"Bloco {index} minerado! Hash: {bloco['hash']}")
    return bloco

def main():
    # Endereço fixo do minerador para deploy
    endereco_minerador = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"

    blockchain = carregar_blockchain()
    print(f"Blockchain carregada com {len(blockchain)} blocos.\n")

    while True:
        try:
            transacoes_pendentes = []  # Pode adicionar transações futuras aqui
            bloco = minerar_bloco(transacoes_pendentes, endereco_minerador, blockchain)
            saldo = calcular_saldo(endereco_minerador, blockchain)
            print(f"Saldo atual do minerador ({endereco_minerador}): {saldo} TiBúrcio\n")
        except Exception as e:
            print(f"Erro ao minerar: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
