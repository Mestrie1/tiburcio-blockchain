import json

ARQUIVO_BLOCKCHAIN = "blockchain.json"

def carregar_blockchain():
    with open(ARQUIVO_BLOCKCHAIN, "r") as f:
        return json.load(f)

def calcular_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        for transacao in bloco.get("transacoes", []):
            if transacao.get("destino") == endereco:
                saldo += transacao.get("quantidade", 0)
            if transacao.get("origem") == endereco:
                saldo -= transacao.get("quantidade", 0)
    return saldo

def main():
    endereco = input("Digite o endereço da carteira para ver saldo: ")
    blockchain = carregar_blockchain()
    saldo = calcular_saldo(blockchain, endereco)
    print(f"💰 Saldo da carteira {endereco}: {saldo} Tibúrcio")

if __name__ == "__main__":
    main()
