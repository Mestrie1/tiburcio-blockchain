from flask import Flask, jsonify
import json
import traceback

app = Flask(__name__)

def carregar_blockchain():
    with open('blockchain.json', 'r') as arquivo:
        return json.load(arquivo)

@app.route('/')
def home():
    return 'Tiburcio Blockchain API'

@app.route('/saldo/<endereco>', methods=['GET'])
def saldo(endereco):
    try:
        blockchain = carregar_blockchain()
        saldo = 0
        for bloco in blockchain:
            transacoes = bloco.get('transacoes', [])
            for transacao in transacoes:
                if transacao.get('de') == endereco:
                    saldo -= transacao.get('quantidade', 0)
                if transacao.get('para') == endereco:
                    saldo += transacao.get('quantidade', 0)
        return jsonify({'endereco': endereco, 'saldo': saldo})

    except Exception as e:
        print("Erro no /saldo:", e)
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
