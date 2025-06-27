import threading
import requests
import time
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Blockchain local (exemplo simplificado)
blockchain = []

# Lista dinâmica de peers (IPs + portas)
peers = set()

# Função para validar blockchain (simplificada)
def validar_blockchain(chain):
    # Aqui você faz validações de hashes, índices, etc.
    return True

# Endpoint para receber blockchain de peer
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify(blockchain)

# Endpoint para receber novo bloco propagado
@app.route('/add_block', methods=['POST'])
def add_block():
    bloco = request.get_json()
    # Validar bloco aqui
    blockchain.append(bloco)
    print(f"Novo bloco adicionado via P2P: {bloco['indice']}")
    # Propaga para os peers
    propagar_bloco(bloco)
    return 'Bloco recebido', 200

# Propagar bloco para os peers
def propagar_bloco(bloco):
    for peer in peers:
        try:
            url = f"{peer}/add_block"
            requests.post(url, json=bloco, timeout=3)
        except Exception as e:
            print(f"Erro ao propagar para {peer}: {e}")

# Função para sincronizar blockchain pegando a maior de todos os peers
def sincronizar():
    global blockchain
    maior_chain = blockchain
    for peer in list(peers):
        try:
            response = requests.get(f"{peer}/blockchain", timeout=5)
            chain_peer = response.json()
            if len(chain_peer) > len(maior_chain) and validar_blockchain(chain_peer):
                maior_chain = chain_peer
        except Exception as e:
            print(f"Erro ao sincronizar com {peer}: {e}")
    if maior_chain != blockchain:
        print("Blockchain atualizada via sincronização P2P.")
        blockchain = maior_chain

# Thread para sincronizar a cada 10 segundos
def sincronizar_periodicamente():
    while True:
        sincronizar()
        time.sleep(10)

# Adicionar peer novo (ex: via linha de comando ou endpoint)
def adicionar_peer(url):
    if url not in peers:
        peers.add(url)
        print(f"Peer adicionado: {url}")

if __name__ == '__main__':
    # Exemplo: adiciona peers manualmente
    adicionar_peer('http://192.168.1.65:5002')
    adicionar_peer('http://192.168.1.66:5002')

    # Inicia thread para sincronizar a blockchain
    thread_sync = threading.Thread(target=sincronizar_periodicamente, daemon=True)
    thread_sync.start()

    # Inicia servidor Flask para comunicação P2P
    app.run(host='0.0.0.0', port=5002)
