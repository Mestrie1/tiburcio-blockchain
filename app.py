from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Simples lista para guardar a blockchain em memória (exemplo)
blockchain = []

@app.route('/blockchain', methods=['GET'])
def mostrar_blockchain():
    return jsonify(blockchain)

@app.route('/novo_bloco', methods=['POST'])
def receber_novo_bloco():
    bloco = request.get_json()
    blockchain.append(bloco)
    return jsonify({'message': 'Bloco adicionado com sucesso!'}), 200

# Aqui podem ser adicionadas outras rotas, tipo consultar saldo, enviar transação, etc.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Porta do Render ou 8080 local
    app.run(host='0.0.0.0', port=port)

