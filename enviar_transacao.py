import json

TRANSACOES_PENDENTES_FILE = "transacoes_pendentes.json"

def carregar_transacoes_pendentes():
    try:
        with open(TRANSACOES_PENDENTES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_transacoes_pendentes(transacoes):
    with open(TRANSACOES_PENDENTES_FILE, "w") as f:
        json.dump(transacoes, f, indent=4)

if __name__ == "__main__":
    de = input("Endereço da carteira remetente: ").strip()
    para = input("Endereço da carteira destinatária: ").strip()
    quantidade = float(input("Quantidade a transferir: "))

    transacoes = carregar_transacoes_pendentes()
    transacoes.append({"de": de, "para": para, "quantidade": quantidade})
    salvar_transacoes_pendentes(transacoes)

    print("📬 Transação criada e adicionada às pendentes com sucesso!")
