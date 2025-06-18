from flask import Flask, request, jsonify

app = Flask(__name__)

blockchain = []  # Simples lista para blocos, só exemplo
transactions = []  # Lista de transações pendentes

@app.route('/nova_transacao', methods=['POST'])
def nova_transacao():
    tx = request.get_json()
    transactions.append(tx)
    return jsonify({'status': 'Transação recebida'}), 201

@app.route('/novo_bloco', methods=['POST'])
def novo_bloco():
    bloco = request.get_json()
    blockchain.append(bloco)
    # Após adicionar bloco, limpamos as transações pendentes para simular mineração
    transactions.clear()
    return jsonify({'status': 'Bloco adicionado'}), 201

@app.route('/transacoes_pendentes', methods=['GET'])
def transacoes_pendentes():
    return jsonify(transactions), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
