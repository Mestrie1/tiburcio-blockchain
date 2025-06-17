from flask import Flask
import threading
import time
import json
import os

app = Flask(__name__)

# Nome do arquivo de saldos
SALDO_FILE = "saldos.json"
ENDERECO_MINERADOR = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"

# Função para carregar saldos
def carregar_saldos():
    if os.path.exists(SALDO_FILE):
        with open(SALDO_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

# Função para salvar saldos
def salvar_saldos(saldos):
    with open(SALDO_FILE, "w") as f:
        json.dump(saldos, f)

@app.route("/")
def home():
    return "Minerador Tibúrcio está online!"

def main():
    bloco_atual = 0
    dificuldade = 5
    recompensa = 50

    while True:
        print(f"💎 Minerando bloco {bloco_atual} com dificuldade {dificuldade}...")
        time.sleep(3)
        print(f"💎 Bloco {bloco_atual} minerado! Recompensa: {recompensa} TiBúrcio")

        # Atualiza saldo
        saldos = carregar_saldos()
        if ENDERECO_MINERADOR in saldos:
            saldos[ENDERECO_MINERADOR] += recompensa
        else:
            saldos[ENDERECO_MINERADOR] = recompensa
        salvar_saldos(saldos)

        bloco_atual += 1

def rodar_minerador():
    main()

if __name__ == "__main__":
    minerador_thread = threading.Thread(target=rodar_minerador)
    minerador_thread.daemon = True
    minerador_thread.start()
    app.run(host="0.0.0.0", port=10000)
