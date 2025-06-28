from flask import Flask, jsonify, request
import json
import os
import traceback

app = Flask(__name__)
PASTA_BLOCOS = "blocos"
PENDENTES_FILE = "transacoes_pendentes.json"

def carregar_blocos_individuais():
    blocos = []
    if not os.path.exists(PASTA_BLOCOS):
        return blocos

    for arquivo in os.listdir(PASTA_BLOCOS):
        caminho = os.path.join(PASTA_BLOCOS, arquivo)
        if not arquivo.endswith(".json"):
            continue
        try:
            with open(caminho, "r") as f:
                bloco = json.load(f)
                blocos.append(bloco)
        except Exception as e:
            print(f"Erro ao carregar {arquivo}: {e}")
            continue

    # Ordenar blocos por índice
    blocos.sort(key=lambda b: b.get("indice", 0))
    return blocos

@app.route('/')
def home():
    return 'Tiburcio Blockchain API - Lendo blocos por hash e transações pendentes'

@app.route('/saldo/<endereco>', methods=['GET'])
def saldo(endereco):
    try:
        blockchain = carregar_blocos_individuais()
        saldo = 0
        for bloco in blockchain:
            for tx in bloco.get('transacoes', []):
                if tx.get('de') == endereco:
                    saldo -= tx.get('quantidade', 0)
                if tx.get('para') == endereco:
                    saldo += tx.get('quantidade', 0)
        return jsonify({'endereco': endereco, 'saldo': saldo})
    except Exception as e:
        print("Erro no /saldo:", e)
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno no servidor'}), 500

@app.route('/enviar_transacao', methods=['POST'])
def receber_transacao():
    try:
        dados = request.get_json()
        print("Transação recebida:", dados)

        # Carrega pendentes existentes
        if os.path.exists(PENDENTES_FILE):
            with open(PENDENTES_FILE, "r") as f:
                pendentes = json.load(f)
        else:
            pendentes = []

        # Adiciona nova transação
        pendentes.append(dados)

        # Salva de volta no arquivo
        with open(PENDENTES_FILE, "w") as f:
            json.dump(pendentes, f, indent=4)

        return jsonify({'status': 'transação recebida com sucesso'})
    except Exception as e:
        print("Erro no /enviar_transacao:", e)
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
