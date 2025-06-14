import json

ARQUIVO_BLOCKCHAIN = "blockchain.json"

def carregar_blockchain():
    with open(ARQUIVO_BLOCKCHAIN, "r") as f:
        return json.load(f)

def calcular_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        transacoes = bloco.get("transacoes", [])
        for tx in transacoes:
            if tx.get("destino") == endereco:
                saldo += tx.get("quantidade", 0)
            if tx.get("origem") == endereco:
                saldo -= tx.get("quantidade", 0)
    return saldo

def main():
    blockchain = carregar_blockchain()
    endereco = input("Digite o endereço da carteira para ver saldo: ").strip()
    saldo = calcular_saldo(blockchain, endereco)
    print(f"Saldo da carteira {endereco}: {saldo} TiBúrcio")

if __name__ == "__main__":
    main()
