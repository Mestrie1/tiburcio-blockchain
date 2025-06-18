import json
import time

TRANSACOES_PENDENTES = "transacoes_pendentes.json"

def carregar_transacoes_pendentes():
    try:
        with open(TRANSACOES_PENDENTES, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_transacoes_pendentes(transacoes):
    with open(TRANSACOES_PENDENTES, "w") as f:
        json.dump(transacoes, f, indent=4)

def criar_transacao(de, para, quantidade):
    return {
        "de": de,
        "para": para,
        "quantidade": quantidade,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    endereco_de = input("Endereço da carteira remetente: ").strip()
    endereco_para = input("Endereço da carteira destinatária: ").strip()
    quantidade = float(input("Quantidade a transferir: "))

    transacoes = carregar_transacoes_pendentes()
    transacao = criar_transacao(endereco_de, endereco_para, quantidade)
    transacoes.append(transacao)
    salvar_transacoes_pendentes(transacoes)

    print("Transação criada e adicionada às pendentes com sucesso!")
