import json

ARQUIVO_BLOCKCHAIN = "blockchain.json"

def carregar_blockchain():
    try:
        with open(ARQUIVO_BLOCKCHAIN, "r") as f:
            return json.load(f)
    except:
        return []

def consultar_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0
    for bloco in blockchain:
        for tx in bloco["transacoes"]:
            if tx["para"] == endereco:
                saldo += tx["quantidade"]
            if tx["de"] == endereco:
                saldo -= tx["quantidade"]
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço da carteira para consultar saldo: ").strip()
    saldo = consultar_saldo(endereco)
    print(f"Saldo da carteira {endereco}: {saldo} tokens")

