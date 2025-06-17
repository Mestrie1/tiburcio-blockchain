from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Minerador Tibúrcio está online!"

def main():
    # Aqui você coloca a lógica do seu minerador
    # Exemplo básico de loop de mineração (substitua pela sua função real)
    import time
    bloco_atual = 0
    dificuldade = 5
    while True:
        print(f"Minerando bloco {bloco_atual} com dificuldade {dificuldade}...")
        # Simule mineração
        time.sleep(5)
        print(f"Bloco {bloco_atual} minerado!")
        bloco_atual += 1

def rodar_minerador():
    main()

if __name__ == "__main__":
    minerador_thread = threading.Thread(target=rodar_minerador)
    minerador_thread.daemon = True
    minerador_thread.start()
    app.run(host="0.0.0.0", port=10000)

