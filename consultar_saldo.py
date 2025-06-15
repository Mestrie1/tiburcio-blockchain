import json
import os

CAMINHO_BLOCKCHAIN = 'blockchain.json'

def carregar_blockchain():
    if not os.path.exists(CAMINHO_BLOCKCHAIN):
        return []
    with open(CAMINHO_BLOCKCHAIN, 'r') as f:
        return json.load(f)

def calcular_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0

    for bloco in blockchain:
        recompensa = bloco.get('recompensa')
        if recompensa and recompensa.get('para') == endereco:
            saldo += recompensa.get('quantidade', 0)

        transacoes = bloco.get('transacoes', [])
        for tx in transacoes:
            if tx.get('de') == endereco:
                saldo -= tx.get('quantidade', 0)
            if tx.get('para') == endereco:
                saldo += tx.get('quantidade', 0)

    return saldo

if __name__ == '__main__':
    endereco = input('Digite o endereço da carteira para ver saldo: ').strip()
    saldo = calcular_saldo(endereco)
    print(f'💰 Saldo da carteira {endereco}: {saldo} Tibúrcio')
