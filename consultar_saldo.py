def calcular_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        # Se existir recompensa como dict e o endereço for o destino
        recompensa = bloco.get("recompensa")
        if isinstance(recompensa, dict) and recompensa.get("para") == endereco:
            saldo += recompensa.get("quantidade", 0)

        # Se existir lista de transações
        transacoes = bloco.get("transacoes", [])
        for tx in transacoes:
            if tx.get("destino") == endereco:
                saldo += tx.get("quantidade", 0)
            if tx.get("origem") == endereco:
                saldo -= tx.get("quantidade", 0)
    return saldo
