def calcular_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        transacoes = bloco.get("transacoes", [])
        for tx in transacoes:
            if tx.get("origem") == endereco:
                saldo -= tx.get("quantidade", 0)
            if tx.get("destino") == endereco:
                saldo += tx.get("quantidade", 0)
    return saldo
