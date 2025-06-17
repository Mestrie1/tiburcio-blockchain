from flask import Flask
import threading
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "Minerador Tibúrcio está online!"

def main():
    bloco_atual = 0
    dificuldade = 5
    tempo_alvo = 10  # segundos, ajuste conforme desejar
    blocos_por_ajuste = 5

    tempos = []

    while True:
        print(f"Minerando bloco {bloco_atual} com dificuldade {dificuldade}...")
        inicio = time.time()

        # Simular mineração: aqui você colocaria o código real de mineração
        time.sleep(tempo_alvo - 2)  # só para simular um tempo variável
        # --- Fim da simulação ---

        fim = time.time()
        duracao = fim - inicio
        tempos.append(duracao)

        print(f"Bloco {bloco_atual} minerado em {duracao:.2f} segundos!")
        bloco_atual += 1

        # Ajustar dificuldade a cada blocos_por_ajuste blocos
        if bloco_atual % blocos_por_ajuste == 0:
            tempo_medio = sum(tempos) / len(tempos)
            print(f"Tempo médio dos últimos {blocos_por_ajuste} blocos: {tempo_medio:.2f}s")

            if tempo_medio < tempo_alvo:
                dificuldade += 1
                print(f"Aumentando dificuldade para {dificuldade}")
            elif tempo_medio > tempo_alvo and dificuldade > 1:
                dificuldade -= 1
                print(f"Diminuindo dificuldade para {dificuldade}")

            tempos = []  # resetar lista

def rodar_minerador():
    main()

if __name__ == "__main__":
    minerador_thread = threading.Thread(target=rodar_minerador)
    minerador_thread.daemon = True
    minerador_thread.start()
    app.run(host="0.0.0.0", port=10000)
