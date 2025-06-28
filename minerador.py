import json
import time
import hashlib
import base64
import os
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

# Configurações básicas
PASTA_BLOCOS = "blocos"
if not os.path.exists(PASTA_BLOCOS):
    os.makedirs(PASTA_BLOCOS)

TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"

RECOMPENSA_INICIAL = 50
INTERVALO_HALVING = 210000
SUPPLY_MAXIMO = 21000000
TARGET_INTERVALO = 10 * 60  # 10 minutos por bloco
DIFICULDADE_RECALCULO = 2016  # Blocos entre ajuste de dificuldade
TEMPO_ALVO_2016_BLOCOS = DIFICULDADE_RECALCULO * TARGET_INTERVALO  # ~2 semanas

# Salva o bloco individualmente e atualiza o último bloco
def salvar_bloco_individual(bloco):
    hash_bloco = bloco['hash']
    caminho = os.path.join(PASTA_BLOCOS, f"{hash_bloco}.json")
    with open(caminho, "w") as f:
        json.dump(bloco, f, indent=4)
    with open("ultimo_bloco.txt", "w") as f:
        f.write(hash_bloco)
    print(f"Bloco salvo: {caminho}")

# Carrega o último bloco salvo (pelo arquivo índice)
def carregar_ultimo_bloco():
    try:
        with open("ultimo_bloco.txt", "r") as f:
            hash_ultimo = f.read().strip()
        caminho = os.path.join(PASTA_BLOCOS, f"{hash_ultimo}.json")
        with open(caminho, "r") as f:
            bloco = json.load(f)
        return bloco
    except FileNotFoundError:
        return None

# Carrega o bloco pelo hash
def carregar_bloco(hash_bloco):
    caminho = os.path.join(PASTA_BLOCOS, f"{hash_bloco}.json")
    with open(caminho, "r") as f:
        bloco = json.load(f)
    return bloco

# Função para carregar bloco pelo índice - busca na pasta blocos
def carregar_bloco_por_indice(indice):
    for arquivo in os.listdir(PASTA_BLOCOS):
        caminho = os.path.join(PASTA_BLOCOS, arquivo)
        with open(caminho, "r") as f:
            bloco = json.load(f)
            if bloco["indice"] == indice:
                return bloco
    raise Exception(f"Bloco com índice {indice} não encontrado.")

# Cria o bloco gênesis se não existir blockchain
def criar_bloco_genesis():
    bloco_genesis = {
        "indice": 0,
        "transacoes": [],
        "anterior": "0" * 64,
        "nonce": 0,
        "timestamp": time.time(),
        "hash": "",
        "dificuldade": 4  # dificuldade inicial
    }
    bloco_genesis["hash"] = calcular_hash(bloco_genesis)
    salvar_bloco_individual(bloco_genesis)
    return bloco_genesis

# Calcula o hash do bloco (sem considerar o campo hash)
def calcular_hash(bloco):
    bloco_copy = dict(bloco)
    bloco_copy.pop("hash", None)
    bloco_str = json.dumps(bloco_copy, sort_keys=True).encode()
    return hashlib.sha256(bloco_str).hexdigest()

# Calcula a dificuldade atual, recalculada a cada 2016 blocos
def calcular_dificuldade():
    ultimo_bloco = carregar_ultimo_bloco()
    if ultimo_bloco is None:
        return 4  # dificuldade inicial
    
    indice_atual = ultimo_bloco["indice"]

    # Se ainda não chegou ao intervalo para recalcular, retorna dificuldade do último bloco
    if indice_atual == 0 or indice_atual % DIFICULDADE_RECALCULO != 0:
        return ultimo_bloco.get("dificuldade", 4)
    
    # Hora de recalcular a dificuldade
    bloco_inicio = carregar_bloco_por_indice(indice_atual - DIFICULDADE_RECALCULO + 1)
    bloco_fim = ultimo_bloco

    tempo_real = bloco_fim["timestamp"] - bloco_inicio["timestamp"]

    # Limita o tempo real para evitar mudanças extremas
    minimo = TEMPO_ALVO_2016_BLOCOS // 4
    maximo = TEMPO_ALVO_2016_BLOCOS * 4
    tempo_real = max(min(tempo_real, maximo), minimo)

    dificuldade_atual = bloco_inicio.get("dificuldade", 4)
    nova_dificuldade = int(dificuldade_atual * (TEMPO_ALVO_2016_BLOCOS / tempo_real))
    nova_dificuldade = max(1, nova_dificuldade)
    print(f"Dificuldade recalculada: {nova_dificuldade} (anterior: {dificuldade_atual}, tempo_real: {tempo_real:.0f}s)")
    return nova_dificuldade

# Prova de trabalho com dificuldade dinâmica (prefixo zeros)
def prova_de_trabalho(bloco, dificuldade):
    bloco["nonce"] = 0
    prefixo = "0" * dificuldade
    while True:
        bloco["hash"] = calcular_hash(bloco)
        if bloco["hash"].startswith(prefixo):
            bloco["dificuldade"] = dificuldade
            return bloco
        bloco["nonce"] += 1

# Função para carregar transações pendentes
def carregar_transacoes_pendentes():
    try:
        with open(TRANSACOES_PENDENTES_FILE, "r") as f:
            transacoes = json.load(f)
            return transacoes if isinstance(transacoes, list) else []
    except FileNotFoundError:
        return []

# Função para salvar transações pendentes
def salvar_transacoes_pendentes(transacoes):
    with open(TRANSACOES_PENDENTES_FILE, "w") as f:
        json.dump(transacoes, f, indent=4)

# Função para calcular recompensa (halving a cada 210000 blocos)
def calcular_recompensa(indice_bloco):
    halvings = indice_bloco // INTERVALO_HALVING
    recompensa = RECOMPENSA_INICIAL // (2 ** halvings)
    return max(recompensa, 1)

# Função para calcular total minerado (somando blocos individuais)
def calcular_total_minerado():
    total = 0
    for arquivo in os.listdir(PASTA_BLOCOS):
        caminho = os.path.join(PASTA_BLOCOS, arquivo)
        with open(caminho, "r") as f:
            bloco = json.load(f)
            for tx in bloco["transacoes"]:
                if tx.get("de") == "RECOMPENSA":
                    total += tx["quantidade"]
    return total

# Função para validar assinatura das transações
def validar_assinatura(tx):
    try:
        remetente = tx["de"]
        destinatario = tx["para"]
        quantidade = tx["quantidade"]
        assinatura_b64 = tx["assinatura"]
        chave_publica_hex = tx["chave_publica"]

        mensagem = f"remetente:{remetente};destinatario:{destinatario};quantidade:{quantidade}"
        hash_mensagem = hashlib.sha256(mensagem.encode()).digest()

        assinatura = base64.b64decode(assinatura_b64)
        chave_publica_bytes = bytes.fromhex(chave_publica_hex)
        vk = VerifyingKey.from_string(chave_publica_bytes, curve=SECP256k1)
        vk.verify(assinatura, hash_mensagem)
        return True
    except (BadSignatureError, KeyError, ValueError):
        return False

# Função para minerar bloco com dificuldade dinâmica
def minerar_bloco(carteira_minerador):
    ultimo_bloco = carregar_ultimo_bloco()
    if ultimo_bloco is None:
        ultimo_bloco = criar_bloco_genesis()
    
    novo_indice = ultimo_bloco["indice"] + 1
    dificuldade_atual = calcular_dificuldade()

    transacoes_pendentes = carregar_transacoes_pendentes()
    transacoes_validas = [tx for tx in transacoes_pendentes if validar_assinatura(tx)]

    total_minerado = calcular_total_minerado()
    recompensa_atual = calcular_recompensa(novo_indice)

    if total_minerado >= SUPPLY_MAXIMO:
        print("💰 Supply máximo alcançado! Não há mais recompensas.")
        recompensa_atual = 0
    elif total_minerado + recompensa_atual > SUPPLY_MAXIMO:
        recompensa_atual = SUPPLY_MAXIMO - total_minerado

    if recompensa_atual > 0:
        transacoes_validas.append({
            "de": "RECOMPENSA",
            "para": carteira_minerador,
            "quantidade": recompensa_atual
        })

    novo_bloco = {
        "indice": novo_indice,
        "transacoes": transacoes_validas,
        "anterior": ultimo_bloco["hash"],
        "nonce": 0,
        "timestamp": time.time(),
        "hash": "",
        "dificuldade": dificuldade_atual
    }

    print(f"🔨 Minerando bloco {novo_indice} com dificuldade {dificuldade_atual}...")
    bloco_minerado = prova_de_trabalho(novo_bloco, dificuldade_atual)

    salvar_bloco_individual(bloco_minerado)
    salvar_transacoes_pendentes([])

    print(f"✅ Bloco {novo_indice} minerado! Recompensa: {recompensa_atual} tokens. Hash: {bloco_minerado['hash']}")

def main():
    print("=== Iniciando minerador do Tibúrcio Blockchain com dificuldade dinâmica ===")
    carteira_minerador = input("🔑 Informe o seu endereço público para receber recompensas: ").strip()
    while len(carteira_minerador) == 0:
        carteira_minerador = input("⚠️ Endereço inválido. Informe novamente: ").strip()
    while True:
        minerar_bloco(carteira_minerador)
        time.sleep(2)

if __name__ == "__main__":
    main()
