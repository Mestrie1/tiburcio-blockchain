import json
import os
import time
import hashlib

CAMINHO_BLOCKCHAIN = 'blockchain.json'

def carregar_blockchain():
    if not os.path.exists(CAMINHO_BLOCKCHAIN):
        return []
    with open(CAMINHO_BLOCKCHAIN, 'r') as f:
        return json.load(f)

def salvar_blockchain(blockchain):
    with open(CAMINHO_BLOCKCHAIN, 'w') as f:
        json.dump(blockchain, f, indent=4)

def calcular_saldo(endereco, blockchain):
    saldo = 0
    for bloco in blockchain:
        recompensa = bloco.get('recompensa')
        if recompensa and recompensa.get('para') == endereco:
            saldo += recompensa.get('quantidade', 0)

        for tx in bloco.get('transacoes', []):
            if tx.get('de') == endereco:
                saldo -= tx.get('quantidade', 0)
            if tx.get('para') == endereco:
                saldo += tx.get('quantidade', 0)
    return saldo

def calcular_hash_bloco(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

def criar_bloco(novo_index, anterior_hash, transacoes):
    timestamp = time.time()
    recompensa = None  # Blocos de transação não geram recompensa para minerador
    bloco = {
        'index': novo_index,
        'timestamp': timestamp,
        'transacoes': transacoes,
        'recompensa': recompensa,
        'anterior': anterior_hash
    }
    bloco['hash'] = calcular_hash_bloco(bloco)
    return bloco

def transferir(de, para, quantidade):
    blockchain = carregar_blockchain()
    saldo_remetente = calcular_saldo(de, blockchain)

    if saldo_remetente < quantidade:
        print(f"❌ Saldo insuficiente. Saldo atual: {saldo_remetente} TiBúrcio.")
        return

    transacao = {
        'de': de,
        'para': para,
        'quantidade': quantidade
    }

    if blockchain:
        ultimo_bloco = blockchain[-1]
        novo_index = ultimo_bloco['index'] + 1
        anterior_hash = ultimo_bloco['hash']
    else:
        novo_index = 0
        anterior_hash = '0'

    novo_bloco = criar_bloco(novo_index, anterior_hash, [transacao])
    blockchain.append(novo_bloco)
    salvar_blockchain(blockchain)
    print(f'✅ Transferência registrada com sucesso! {quantidade} TiBúrcio enviado de {de} para {para}.')

if __name__ == '__main__':
    de = input("Endereço de envio (sua carteira): ").strip()
    para = input("Endereço de destino: ").strip()
    quantidade = float(input("Quantidade a transferir: "))
    transferir(de, para, quantidade)
