import hashlib
import time
import threading
from flask import Flask

app = Flask(__name__)

blockchain = []
difficulty = 4  # Começa com 4 zeros, podemos aumentar isso automaticamente depois

def create_genesis_block():
    return {
        'index': 0,
        'timestamp': time.time(),
        'data': 'Genesis Block',
        'previous_hash': '0',
        'nonce': 0,
        'hash': '0'
    }

def calculate_hash(index, timestamp, data, previous_hash, nonce):
    value = f"{index}{timestamp}{data}{previous_hash}{nonce}".encode()
    return hashlib.sha256(value).hexdigest()

def mine_block(previous_block, data):
    index = previous_block['index'] + 1
    timestamp = time.time()
    previous_hash = previous_block['hash']
    nonce = 0

    prefix = '0' * difficulty
    while True:
        hash_value = calculate_hash(index, timestamp, data, previous_hash, nonce)
        if hash_value.startswith(prefix):
            return {
                'index': index,
                'timestamp': timestamp,
                'data': data,
                'previous_hash': previous_hash,
                'nonce': nonce,
                'hash': hash_value
            }
        nonce += 1

def adjust_difficulty():
    global difficulty
    if len(blockchain) % 5 == 0 and len(blockchain) != 0:
        difficulty += 1
        print(f"Aumentando dificuldade para: {difficulty}")

def minerador():
    global blockchain
    if not blockchain:
        blockchain.append(create_genesis_block())

    while True:
        data = "Bloco minerado Tibúrcio"
        block = mine_block(blockchain[-1], data)
        blockchain.append(block)
        print(f"⛏️ Novo bloco minerado: {block['hash']} | Dificuldade: {difficulty} | Bloco #{block['index']}")
        adjust_difficulty()

@app.route("/")
def home():
    return f"⚡ Minerador Tibúrcio está online! Blocos minerados: {len(blockchain)} | Dificuldade atual: {difficulty}"

if __name__ == "__main__":
    threading.Thread(target=minerador, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
    
