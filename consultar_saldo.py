def calcular_saldo(blockchain, endereco):
    saldo = 0
    for bloco in blockchain:
        # Verifica se 'recompensa' é um dicionário com a chave 'para'
        recompensa = bloco.get("recompensa")
        if isinstance(recompensa, dict):
            if recompensa.get("para") == endereco:
                saldo += recompensa.get("quantidade", 0)
        else:
            # Caso 'recompensa' seja um valor numérico, ignore ou trate se desejar
            pass
        
        # Agora soma as transações normais, se existirem
        for tx in bloco.get("transacoes", []):
            if tx.get("origem") == endereco:
                saldo -= tx.get("quantidade", 0)
            if tx.get("destino") == endereco:
                saldo += tx.get("quantidade", 0)
    return saldo
