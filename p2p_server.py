import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5000

def handle_client(conn, addr):
    print(f"Nova conexão de {addr}")
    data = conn.recv(4096)
    if data:
        try:
            tx = json.loads(data.decode())
            print("Transação recebida:", tx)
            # Aqui futuramente podemos validar a transação e incluir no blockchain
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON recebido")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor P2P ouvindo em {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
