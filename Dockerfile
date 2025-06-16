# Usar imagem oficial do Python 3.10 slim
FROM python:3.10-slim

# Definir diretório da aplicação dentro do container
WORKDIR /app

# Copiar todos os arquivos do seu repositório para dentro do container
COPY . .

# Instalar dependências, caso tenha requirements.txt (se não, pode remover esta linha)
RUN pip install -r requirements.txt || echo "Sem requirements.txt, ignorando"

# Comando para rodar seu servidor P2P (ajuste se necessário)
CMD ["python3", "p2p_server.py"]
