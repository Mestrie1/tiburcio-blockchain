import socket
import threading
import json
import requests
from flask import Flask, jsonify, request

# Arquivos usados
TRANSACOES_ARQUIVO = "transacoes_pendentes.json"
BLOCKCHAIN_FILE = "blockchain.json"

# Lista de peers (troque pelos IPs reais dos seus nós)
peers = [
    "http://IP_DO_NO2:5000",
    "http://IP_DO_NO3:5000",
    # Adicione mais peers aqui
]

# ======= Função para carregar blockchain =======
def carregar_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# ======= Função para calcular saldo =======
def calcular_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0
    for bloco in blockchain:
        for tx in bloco.get("transacoes", []):
            if tx.get("para") == endereco:
                saldo += tx.get("quantidade", 0)
            if tx.get("de") == endereco and tx.get("de") != "RECOMPENSA":
                saldo -= tx.get("quantidade", 0)
    return saldo

# ======= Função para salvar transação pendente =======
def salvar_transacao(tx):
    try:
        with open(TRANSACOES_ARQUIVO, "r") as f:
            transacoes = json.load(f)
    except:
        transacoes = []
    transacoes.append(tx)
    with open(TRANSACOES_ARQUIVO, "w") as f:
        json.dump(transacoes, f, indent=4)
    print("Transação salva:", tx)

# ======= Manipulação do Socket TCP para transações pendentes =======
def handle_client(conn, addr):
    print(f"Conexão de {addr}")
    try:
        data = conn.recv(4096)
        if data:
            tx = json.loads(data.decode())
            salvar_transacao(tx)
            conn.send(b"OK")
    except Exception as e:
        print("Erro no socket:", e)
    finally:
        conn.close()

def start_socket_server(host="0.0.0.0", port=5001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Socket TCP rodando em {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# ======= Flask HTTP API =======
app = Flask(__name__)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    try:
        blockchain = carregar_blockchain()
        return jsonify(blockchain)
    except:
        return jsonify([])

@app.route('/saldo/<string:endereco>', methods=['GET'])
def saldo(endereco):
    saldo_atual = calcular_saldo(endereco)
    return jsonify({"endereco": endereco, "saldo": saldo_atual})

# Endpoint para receber blocos de outros peers e salvar
@app.route('/receive_block', methods=['POST'])
def receive_block():
    bloco = request.get_json()
    if not bloco:
        return jsonify({"erro": "Dados do bloco ausentes"}), 400

    blockchain = carregar_blockchain()

    # Verifica se o bloco já existe na blockchain
    if any(b['hash'] == bloco['hash'] for b in blockchain):
        return jsonify({"status": "Bloco já existe"}), 400

    # Aqui você pode adicionar validação do bloco (ex: hash correto, índice, anterior, etc)
    # Por enquanto, só aceita e salva
    blockchain.append(bloco)
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=4)

    # Propaga o bloco para os peers em thread separada para não travar
    threading.Thread(target=propagar_bloco, args=(bloco,)).start()

    print(f"Bloco recebido e salvo: {bloco['hash']}")
    return jsonify({"status": "Bloco recebido e salvo"})

# Função para propagar bloco para outros peers
def propagar_bloco(bloco):
    for peer in peers:
        try:
            url = f"{peer}/receive_block"
            requests.post(url, json=bloco, timeout=5)
            print(f"Bloco propagado para {peer}")
        except Exception as e:
            print(f"Erro ao propagar para {peer}: {e}")

def start_flask_server():
    app.run(host='0.0.0.0', port=5000)

# ======= Rodar os dois servidores juntos =======
if __name__ == "__main__":
    print("Iniciando servidores P2P (Socket TCP + Flask HTTP)...")
    thread_socket = threading.Thread(target=start_socket_server)
    thread_flask = threading.Thread(target=start_flask_server)
    thread_socket.start()
    thread_flask.start()
    thread_socket.join()
    thread_flask.join()
