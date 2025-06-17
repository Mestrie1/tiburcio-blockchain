import socket
import json
import time

def send_transaction(tx, ip, port=5000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(json.dumps(tx).encode())
        s.close()
        print("✅ Transação enviada com sucesso:")
        print(tx)
    except Exception as e:
        print("❌ Erro ao enviar transação:", e)

if __name__ == "__main__":
    ip_do_no = "srv-d18drfp5pdvs73cue7gg.onrender.com"  # seu nó online no Render
    sender = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"  # seu endereço remetente
    recipient = "2ZaDcYVC9YmPZzLMLqiL4BxiesGBKuPdn1Go5oM16N2RE8N6X9"  # endereço destinatário
    amount = 10  # quantidade de tokens a enviar

    tx = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "timestamp": int(time.time())
    }

    send_transaction(tx, ip=ip_do_no)
