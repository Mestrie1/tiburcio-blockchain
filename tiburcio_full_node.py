import argparse
import threading
import time
import json
import hashlib
import base64
import socket
from flask import Flask, jsonify, request
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

BLOCKCHAIN_FILE = "blockchain.json"
TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"
BACKUP_DIR = "backups"

RECOMPENSA_INICIAL = 50
INTERVALO_HALVING = 210000
SUPPLY_MAXIMO = 21000000
DIFICULDADE = 4  # Quantidade de zeros no início do hash

import os
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# --- Blockchain e transações ---

def carregar_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        # Cria bloco gênesis se não existir
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

def calcular_total_minerado(blockchain):
    total = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx.get("de") == "RECOMPENSA":
                total += tx.get("quantidade", 0)
    return total

def calcular_recompensa(indice_bloco):
    halvings = indice_bloco // INTERVALO_HALVING
    recompensa = RECOMPENSA_INICIAL // (2 ** halvings)
    return max(recompensa, 1)

def prova_de_trabalho(bloco):
    bloco["nonce"] = 0
    prefixo = "0" * DIFICULDADE
    while True:
        bloco["hash"] = calcular_hash(bloco)
        if bloco["hash"].startswith(prefixo):
            return bloco
        bloco["nonce"] += 1

def fazer_backup():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_file = f"{BACKUP_DIR}/blockchain_backup_{timestamp}.json"
    with open(BLOCKCHAIN_FILE, "r") as original, open(backup_file, "w") as backup:
        backup.write(original.read())
    print(f"🗂️ Backup salvo: {backup_file}")

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

# --- Servidor Flask ---

app = Flask(__name__)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    try:
        blockchain = carregar_blockchain()
        return jsonify(blockchain)
    except:
        return jsonify([])

@app.route('/saldo/<endereco>', methods=['GET'])
def saldo(endereco):
    blockchain = carregar_blockchain()
    saldo_atual = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx.get("para") == endereco:
                saldo_atual += tx.get("quantidade", 0)
            if tx.get("de") == endereco:
                saldo_atual -= tx.get("quantidade", 0)
    return jsonify({"endereco": endereco, "saldo": saldo_atual})

# --- Socket TCP para receber transações pendentes ---

def salvar_transacao(tx):
    transacoes = carregar_transacoes_pendentes()
    transacoes.append(tx)
    salvar_transacoes_pendentes(transacoes)
    print("Transação salva:", tx)

def handle_client(conn, addr):
    print(f"Conexão de {addr}")
    try:
        data = conn.recv(4096)
        if data:
            tx = json.loads(data.decode())
            salvar_transacao(tx)
            conn.send(b"OK")
    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()

def start_socket_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Socket TCP rodando em {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# --- Função de mineração em thread ---

def minerar_continuo(carteira_minerador):
    while True:
        minerar_bloco(carteira_minerador)
        time.sleep(2)

# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Tibúrcio Full Node")
    parser.add_argument('--minerador', default="", help="Endereço da carteira para receber recompensas (deixe vazio para não minerar)")
    parser.add_argument('--porta', default="5002", help="Porta para rodar o servidor Flask e socket")
    args = parser.parse_args()

    carteira = args.minerador
    if carteira == "":
        carteira = input("Digite o endereço da carteira mineradora (ou deixe vazio para não minerar): ").strip()

    porta = int(args.porta)
    print("=== Tibúrcio Full Node ===")
    print(f"Recompensa minerador: {carteira if carteira else 'Nenhuma, só servidor rodando'}")

    # Inicia o servidor socket numa thread
    thread_socket = threading.Thread(target=start_socket_server, args=("0.0.0.0", porta+1), daemon=True)
    thread_socket.start()

    # Inicia o servidor Flask numa thread (não daemon pra manter o main vivo)
    thread_flask = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=porta), daemon=False)
    thread_flask.start()

    # Inicia mineração só se carteira for informada
    if carteira:
        thread_mineracao = threading.Thread(target=minerar_continuo, args=(carteira,), daemon=True)
        thread_mineracao.start()

    thread_flask.join()

if __name__ == "__main__":
    main()

