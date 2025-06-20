import socket
import threading
import json

TRANSACOES_ARQUIVO = "transacoes_pendentes.json"

def salvar_transacao(tx):
    try:
        with open(TRANSACOES_ARQUIVO, "r") as f:
            transacoes = json.load(f)
    except:
        transacoes = []
    transacoes.append(tx)
    with open(TRANSACOES_ARQUIVO, "w") as f:
        json.dump(transacoes, f, indent=4)
    print("Transação salva:", tx)

def handle_client(conn, addr):
    print(f"Conexão de {addr}")
    try:
        data = conn.recv(4096)
        if data:
            tx = json.loads(data.decode())
            salvar_transacao(tx)
            conn.send(b"OK")
    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()

def start_server(host="0.0.0.0", port=5001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Servidor rodando em {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
