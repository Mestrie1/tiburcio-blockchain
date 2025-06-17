import json

blockchain_file = "blockchain.json"
carteira = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"

def calcular_saldo():
    saldo = 0
    try:
        with open(blockchain_file, "r") as f:
            blockchain = json.load(f)
            for bloco in blockchain:
                for transacao in bloco.get("transactions", []):
                    if transacao["to"] == carteira:
                        saldo += transacao["amount"]
        return saldo
    except FileNotFoundError:
        return 0

print(f"💰 Saldo da carteira {carteira}: {calcular_saldo()} TiBúrcio")
