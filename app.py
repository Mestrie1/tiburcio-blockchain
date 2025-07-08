from flask import Flask, jsonify, request
import json
import os
import traceback

app = Flask(__name__)

PASTA_BLOCOS = "blocos"
PENDENTES_FILE = "transacoes_pendentes.json"
NFTS_FILE = "nft_loja.json"
NFTS_CARTEIRAS_FILE = "nft_carteiras.json"

# === Carrega todos os blocos salvos individualmente ===
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

    blocos.sort(key=lambda b: b.get("indice", 0))
    return blocos

# === Página inicial ===
@app.route('/')
def home():
    return 'Tiburcio Blockchain API - Blocos, Transações, NFTs'

# === Ver saldo de uma carteira ===
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

# === Enviar uma transação (pendente) ===
@app.route('/enviar_transacao', methods=['POST'])
def receber_transacao():
    try:
        dados = request.get_json()
        print("Transação recebida:", dados)

        if os.path.exists(PENDENTES_FILE):
            with open(PENDENTES_FILE, "r") as f:
                pendentes = json.load(f)
        else:
            pendentes = []

        pendentes.append(dados)

        with open(PENDENTES_FILE, "w") as f:
            json.dump(pendentes, f, indent=4)

        return jsonify({'status': 'transação recebida com sucesso'})
    except Exception as e:
        print("Erro no /enviar_transacao:", e)
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno no servidor'}), 500

# === Ver todos os NFTs disponíveis na loja ===
@app.route('/nfts', methods=['GET'])
def listar_nfts():
    if not os.path.exists(NFTS_FILE):
        return jsonify([])
    with open(NFTS_FILE) as f:
        return jsonify(json.load(f))

# === Comprar um NFT com saldo Tibúrcio ===
@app.route('/comprar_nft', methods=['POST'])
def comprar_nft():
    try:
        dados = request.get_json()
        carteira = dados.get("carteira")
        chave_privada = dados.get("chave_privada")  # opcional
        id_nft = str(dados.get("id_nft"))

        if not os.path.exists(NFTS_FILE):
            return jsonify({"erro": "Loja indisponível."}), 400

        with open(NFTS_FILE) as f:
            loja = json.load(f)

        nft = next((n for n in loja if str(n["id"]) == id_nft), None)
        if not nft:
            return jsonify({"erro": "NFT não encontrado."}), 404

        # Calcular saldo
        blockchain = carregar_blocos_individuais()
        saldo = 0
        for bloco in blockchain:
            for tx in bloco.get("transacoes", []):
                if tx.get("de") == carteira:
                    saldo -= tx.get("quantidade", 0)
                if tx.get("para") == carteira:
                    saldo += tx.get("quantidade", 0)

        preco = nft["preco"]
        if saldo < preco:
            return jsonify({"erro": "Saldo insuficiente."}), 400

        # Criar transação
        nova_tx = {
            "de": carteira,
            "para": "LOJA_NFT_TIBURCIO",
            "quantidade": preco,
            "descricao": f"Compra do NFT ID {id_nft}"
        }

        if os.path.exists(PENDENTES_FILE):
            with open(PENDENTES_FILE, "r") as f:
                pendentes = json.load(f)
        else:
            pendentes = []

        pendentes.append(nova_tx)
        with open(PENDENTES_FILE, "w") as f:
            json.dump(pendentes, f, indent=4)

        # Salvar NFT na carteira
        if os.path.exists(NFTS_CARTEIRAS_FILE):
            with open(NFTS_CARTEIRAS_FILE, "r") as f:
                nfts_carteira = json.load(f)
        else:
            nfts_carteira = {}

        if carteira not in nfts_carteira:
            nfts_carteira[carteira] = []

        nfts_carteira[carteira].append(nft)

        with open(NFTS_CARTEIRAS_FILE, "w") as f:
            json.dump(nfts_carteira, f, indent=4)

        return jsonify({"status": "NFT comprado com sucesso!", "nft": nft})

    except Exception as e:
        print("Erro ao comprar NFT:", e)
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno ao comprar NFT'}), 500

# === Ver todos os NFTs que uma carteira possui ===
@app.route('/meus_nfts/<carteira>', methods=['GET'])
def meus_nfts(carteira):
    if not os.path.exists(NFTS_CARTEIRAS_FILE):
        return jsonify([])
    with open(NFTS_CARTEIRAS_FILE, "r") as f:
        dados = json.load(f)
    return jsonify(dados.get(carteira, []))

# === Rodar servidor na porta 8082 ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)

