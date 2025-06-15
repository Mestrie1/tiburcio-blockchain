def criar_transacao(blockchain, origem, destino, quantidade):
    saldo_origem = consultar_saldo(blockchain, origem)
    if saldo_origem < quantidade:
        print("Saldo insuficiente!")
        return None
    return {"origem": origem, "destino": destino, "quantidade": quantidade}
