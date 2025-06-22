import requests
import json

BLOCKCHAIN_FILE = "blockchain.json"

def baixar_blockchain(url_nodo):
    try:
        resposta = requests.get(f"{url_nodo}/blockchain")
        nova_blockchain = resposta.json()

        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump(nova_blockchain, f, indent=4)

        print("✅ Blockchain sincronizada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao sincronizar: {e}")

if __name__ == "__main__":
    url = input("🌐 URL do nó para sincronizar (ex: http://IP:5000): ").strip()
    baixar_blockchain(url)
