import os
from flask import Flask, jsonify, request

app = Flask(__name__)
blockchain = []

@app.route('/blockchain', methods=['GET'])
def mostrar_blockchain():
    return jsonify(blockchain)

@app.route('/novo_bloco', methods=['POST'])
def receber_novo_bloco():
    bloco = request.get_json()
    blockchain.append(bloco)
    return jsonify({'message': 'Bloco adicionado com sucesso!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
