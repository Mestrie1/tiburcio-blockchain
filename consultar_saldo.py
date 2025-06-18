import json

def calcular_saldo(endereco):
    try:
        with open('blockchain.json', 'r') as f:
            blockchain = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Blockchain não encontrada ou vazia.")
        return 0

    saldo = 0
    for bloco in blockchain:
        transacoes = bloco.get('transacoes', [])
        for tx in transacoes:
            remetente = tx.get('remetente') or tx.get('de')  # para recompensas
            destinatario = tx.get('destinatario') or tx.get('para')

            if remetente == "RECOMPENSA":
                if destinatario == endereco:
                    saldo += tx.get('quantidade', 0)
            else:
                if remetente == endereco:
                    saldo -= tx.get('quantidade', 0)
                if destinatario == endereco:
                    saldo += tx.get('quantidade', 0)
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço da carteira para ver saldo: ")
    saldo = calcular_saldo(endereco)
    print(f"💰 Saldo da carteira {endereco}: {saldo} TiBúrcio")

