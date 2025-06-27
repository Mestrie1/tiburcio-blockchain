import requests
import json
import os

# Lista de peers (endereços HTTP com porta)
peers = [
    "http://IP_DO_PEER1:5002",
    "http://IP_DO_PEER2:5002",
    # Adicione mais peers aqui
]

BLOCKCHAIN_FILE = "blockchain.json"

def carregar_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def salvar_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f, indent=4)

def validar_blockchain(blockchain):
    # Aqui você pode colocar sua validação (hash, índice, etc)
    # Por enquanto, só retorna True para simplificar
    return True

def sincronizar_blockchain():
    blockchain_local = carregar_blockchain()
    for peer in peers:
        try:
            resposta = requests.get(f"{peer}/blockchain", timeout=5)
            if resposta.status_code == 200:
                blockchain_peer = resposta.json()
                if (len(blockchain_peer) > len(blockchain_local)
                    and validar_blockchain(blockchain_peer)):
                    print(f"Atualizando blockchain local com dados de {peer}")
                    blockchain_local = blockchain_peer
                    salvar_blockchain(blockchain_local)
        except Exception as e:
            print(f"Erro ao sincronizar com {peer}: {e}")

if __name__ == "__main__":
    sincronizar_blockchain()
