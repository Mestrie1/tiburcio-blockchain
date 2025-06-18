from flask import Flask, request, jsonify
from hashlib import sha256
import json
import time

app = Flask(__name__)

blockchain = []
transacoes_pendentes = []

def calcular_hash_bloco(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return sha256(bloco_serializado).hexdigest()

def criar_bloco(transacoes, anterior_hash=''):
    bloco = {
        'index': len(blockchain) + 1,
        'timestamp': time.time(),
        'transacoes': transacoes,
        'anterior_hash': anterior_hash,
    }
    bloco['hash'] = calcular_hash_bloco(bloco)
    return bloco

@app.route('/nova_transacao', methods=['POST'])
def nova_transacao():
    dados = request.get_json()
    required = ['remetente', 'destinatario', 'quantidade', 'assinatura']
    if not all(k in dados for k in required):
        return 'Transação inválida', 400
    transacoes_pendentes.append(dados)
    return jsonify({'status': 'Transação recebida'}), 201

@app.route('/minerar', methods=['GET'])
def minerar():
    if not transacoes_pendentes:
        return jsonify({'status': 'Sem transações para minerar'}), 200

    ultimo_hash = blockchain[-1]['hash'] if blockchain else '0'
    novo_bloco = criar_bloco(transacoes_pendentes.copy(), ultimo_hash)
    blockchain.append(novo_bloco)
    transacoes_pendentes.clear()

    return jsonify({'status': 'Bloco minerado', 'bloco': novo_bloco}), 201

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify(blockchain), 200

@app.route('/transacoes_pendentes', methods=['GET'])
def get_transacoes_pendentes():
    return jsonify(transacoes_pendentes), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

