import json
import time
import hashlib
import base64
import os
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

BLOCKCHAIN_FILE = "blockchain.json"
TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"
BACKUP_DIR = "backups"

RECOMPENSA_INICIAL = 50
INTERVALO_HALVING = 210000
SUPPLY_MAXIMO = 21000000
DIFICULDADE = 4  # Quantidade de zeros iniciais exigidos no hash

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def carregar_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        bloco_genesis = {
            "indice": 0,
            "transacoes": [],
            "anterior": "0" * 64,
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

def fazer_backup():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_file = f"{BACKUP_DIR}/blockchain_backup_{timestamp}.json"
    with open(BLOCKCHAIN_FILE, "r") as original, open(backup_file, "w") as backup:
        backup.write(original.read())
    print(f"🗂️ Backup salvo: {backup_file}")

def carregar_transacoes_pendentes():
    try:
        with open(TRANSACOES_PENDENTES_FILE, "r") as f:
            transacoes = json.load(f)
            return transacoes if isinstance(transacoes, list) else []
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

def calcular_recompensa(indice_bloco):
    halvings = indice_bloco // INTERVALO_HALVING
    recompensa = RECOMPENSA_INICIAL // (2 ** halvings)
    return max(recompensa, 1)

def calcular_total_minerado(blockchain):
    total = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx["de"] == "RECOMPENSA":
                total += tx["quantidade"]
    return total

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

def minerar_bloco(carteira_minerador):
    blockchain = carregar_blockchain()
    transacoes_pendentes = carregar_transacoes_pendentes()

    ultimo_bloco = blockchain[-1]
    novo_indice = ultimo_bloco["indice"] + 1

    total_minerado = calcular_total_minerado(blockchain)
    recompensa_atual = calcular_recompensa(novo_indice)

    if total_minerado >= SUPPLY_MAXIMO:
        print("💰 Supply máximo alcançado! Não há mais recompensas.")
        recompensa_atual = 0
    elif total_minerado + recompensa_atual > SUPPLY_MAXIMO:
        recompensa_atual = SUPPLY_MAXIMO - total_minerado

    transacoes_validas = [tx for tx in transacoes_pendentes if validar_assinatura(tx)]

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
        "hash": ""
    }

    print(f"🔨 Minerando bloco {novo_indice}...")
    bloco_minerado = prova_de_trabalho(novo_bloco)

    blockchain.append(bloco_minerado)
    salvar_blockchain(blockchain)
    fazer_backup()
    salvar_transacoes_pendentes([])

    print(f"✅ Bloco {novo_indice} minerado! Recompensa: {recompensa_atual} tokens. Hash: {bloco_minerado['hash']}")

def main():
    print("=== Iniciando minerador do Tibúrcio Blockchain ===")
    carteira_minerador = input("🔑 Informe o seu endereço público para receber recompensas: ").strip()
    while len(carteira_minerador) == 0:
        carteira_minerador = input("⚠️ Endereço inválido. Informe novamente: ").strip()

    while True:
        minerar_bloco(carteira_minerador)
        time.sleep(2)

if __name__ == "__main__":
    main()

