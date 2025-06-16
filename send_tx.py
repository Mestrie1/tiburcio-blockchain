import socket
import json

def send_transaction(tx, ip='127.0.0.1', port=5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(json.dumps(tx).encode())
    s.close()
    print("Transação enviada:", tx)

if __name__ == "__main__":
    tx = {
        "sender": "endereco_A",
        "recipient": "endereco_B",
        "amount": 10,
        "timestamp": 1234567890
    }
    send_transaction(tx)
Adiciona script send_tx.py para envio de transações P2P
