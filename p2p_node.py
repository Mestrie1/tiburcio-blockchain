import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5001

def handle_client(conn, addr):
    print(f"Nova conexão de {addr}")
    try:
        data = conn.recv(4096)
        if not data:
            print("Nenhum dado recebido.")
            return
        try:
            tx = json.loads(data.decode())
            print("Transação recebida:", tx)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON recebido de {addr}: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Nó P2P ouvindo em {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    start_server()
