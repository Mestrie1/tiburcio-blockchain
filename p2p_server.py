import socket
import threading
import json
from flask import Flask, jsonify

# Arquivos usados
TRANSACOES_ARQUIVO = "transacoes_pendentes.json"
BLOCKCHAIN_FILE = "blockchain.json"

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

# ======= Parte Socket TCP para transações pendentes =======

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

def start_socket_server(host="0.0.0.0", port=5001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Socket TCP rodando em {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# ======= Parte Flask HTTP para servir a blockchain e saldo =======

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
