from flask import Flask
import threading
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "Minerador Tibúrcio está online!"

def main():
    while True:
        print("Minerando...")  # Aqui vai a sua lógica real de mineração
        time.sleep(5)

def rodar_minerador():
    main()

if __name__ == "__main__":
    minerador_thread = threading.Thread(target=rodar_minerador)
    minerador_thread.daemon = True
    minerador_thread.start()
    app.run(host="0.0.0.0", port=10000)
