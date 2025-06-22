#!/bin/bash

# Atualizar pip e instalar dependências
echo "Atualizando pip e instalando dependências..."
pip install --upgrade pip
pip install ecdsa flask

# Verificar e criar arquivos JSON vazios se não existirem
if [ ! -f blockchain.json ]; then
    echo "Criando arquivo blockchain.json vazio..."
    echo "[]" > blockchain.json
fi

if [ ! -f transacoes_pendentes.json ]; then
    echo "Criando arquivo transacoes_pendentes.json vazio..."
    echo "[]" > transacoes_pendentes.json
fi

# Rodar servidor Flask em background
echo "Iniciando servidor Flask (app.py) em background..."
python3 app.py &

# Esperar 3 segundos para servidor iniciar
sleep 3

# Rodar minerador no primeiro plano
echo "Iniciando minerador (minerador.py)..."
python3 minerador.py
