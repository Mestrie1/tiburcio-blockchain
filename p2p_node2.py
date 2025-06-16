import socket
import threading
import json
import time

HOST = '0.0.0.0'
PORT = 5001

peers = [
    ('127.0.0.1', 5000),
]

blockchain = []

def handle_client(conn, addr):
    # código para tratar conexões recebidas
    pass

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

