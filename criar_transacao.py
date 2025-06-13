import json
import sys
import os

# Função para carregar as transações pendentes
def carregar_transacoes_pendentes():
    if not os.path.exists("transacoes_pendentes.txt"):
        return []
    with open("transacoes_pendentes.txt", "r") as f:
        return json.load(f)

# Função para salvar transações pendentes
def salvar_transacoes_pendentes(transacoes):
    with open("transacoes_pendentes.txt", "w") as f:
        json.dump(transacoes, f, indent=4)

if len(sys.argv) != 4:
    print("Uso correto: python criar_transacao.py <origem> <destino> <quantidade>")
    sys.exit(1)

origem = sys.argv[1]
destino = sys.argv[2]
quantidade = float(sys.argv[3])

transacoes = carregar_transacoes_pendentes()

nova_transacao = {
    "origem": origem,
    "destino": destino,
    "quantidade": quantidade
}

transacoes.append(nova_transacao)
salvar_transacoes_pendentes(transacoes)

print(f"Transação de {quantidade} $Tib de {origem} para {destino} criada com sucesso!")
