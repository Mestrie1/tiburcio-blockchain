import requests

URL_SALDO = "http://localhost:5002/saldo"

print("=== Consulta de Saldo Online ===")
endereco = input("Digite o endereço público da carteira: ")

try:
    resposta = requests.get(f"{URL_SALDO}?endereco={endereco}")
    if resposta.status_code == 200:
        dados = resposta.json()
        print(f"Saldo da carteira {endereco}: {dados['saldo']} Tibúrcio")
    else:
        print("Erro ao consultar saldo:", resposta.text)
except Exception as e:
    print("Erro ao conectar ao servidor:", e)

