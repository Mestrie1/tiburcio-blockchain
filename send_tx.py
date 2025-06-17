import socket
import json
import time

def send_transaction(tx, ip='srv-d18drfp5pdvs73cue7gg.onrender.com', port=5000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(json.dumps(tx).encode())
        s.close()
        print("Transação enviada:", tx)
    except Exception as e:
        print("Erro ao enviar transação:", e)

if __name__ == "__main__":
    tx = {
        "sender": "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM",
        "recipient": "2ZaDcYVC9YmPZzLMLqiL4BxiesGBKuPdn1Go5oM16N2RE8N6X9",
        "amount": 10,
        "timestamp": int(time.time())
    }
    send_transaction(tx)
