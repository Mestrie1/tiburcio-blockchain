import json

BLOCKCHAIN_FILE = "blockchain.json"

def carregar_blockchain():
    with open(BLOCKCHAIN_FILE, "r") as f:
        return json.load(f)

def calcular_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx["de"] == endereco:
                saldo -= tx["quantidade"]
            if tx["para"] == endereco:
                saldo += tx["quantidade"]
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço para consultar saldo: ").strip()
    saldo = calcular_saldo(endereco)
    print(f"Saldo da carteira {endereco}: {saldo} tokens")

