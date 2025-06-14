def consultar_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        for transacao in bloco['transacoes']:
            if transacao['destino'] == endereco:
                saldo += transacao['quantidade']
            if transacao['origem'] == endereco:
                saldo -= transacao['quantidade']
    return saldo
