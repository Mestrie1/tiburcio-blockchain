import json

ARQUIVO_TRANSACOES = "transacoes_pendentes.json"

def carregar_transacoes():
    try:
        with open(ARQUIVO_TRANSACOES, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar transações: {e}")
        return []

def salvar_transacoes(transacoes):
    try:
        with open(ARQUIVO_TRANSACOES, "w") as f:
            json.dump(transacoes, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar transações: {e}")

def validar_transacao(tx):
    campos_necessarios = ["de", "para", "quantidade", "assinatura", "chave_publica"]
    for campo in campos_necessarios:
        if campo not in tx:
            return False
    # Você pode adicionar outras validações aqui, se quiser
    return True

def main():
    transacoes = carregar_transacoes()
    print(f"Total transações carregadas: {len(transacoes)}")

    transacoes_validas = []
    transacoes_invalidas = []

    for tx in transacoes:
        if validar_transacao(tx):
            transacoes_validas.append(tx)
        else:
            transacoes_invalidas.append(tx)

    print(f"Transações válidas: {len(transacoes_validas)}")
    print(f"Transações inválidas removidas: {len(transacoes_invalidas)}")

    salvar_transacoes(transacoes_validas)
    print("Arquivo transacoes_pendentes.json atualizado com transações válidas.")

if __name__ == "__main__":
    main()
