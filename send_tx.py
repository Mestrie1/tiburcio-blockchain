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
    ip_do_no = input("Digite o IP ou domínio do seu nó online (ex: render-xyz.onrender.com): ")
    sender = input("Digite o endereço remetente: ")
    recipient = input("Digite o endereço destinatário: ")
    try:
        amount = float(input("Digite a quantidade a enviar: "))
    except:
        print("Quantidade inválida. Use apenas números.")
        exit(1)

    tx = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "timestamp": int(time.time())
    }

    send_transaction(tx, ip=ip_do_no)
