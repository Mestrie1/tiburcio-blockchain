# Usar imagem oficial do Python 3.10 slim
FROM python:3.10-slim

# Criar diretório da aplicação dentro do container
WORKDIR /app

# Copiar todos os arquivos do seu repo para o container
COPY . .

# Caso tenha dependências em requirements.txt (se não tiver, pode ignorar essa linha)
# RUN pip install -r requirements.txt

# Comando para rodar seu servidor P2P (ajuste se seu arquivo principal for outro)
CMD ["python3", "p2p_server.py"]
