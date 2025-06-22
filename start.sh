#!/bin/bash

# Verifica se Python, pip e módulos necessários estão instalados
echo "🔧 Verificando dependências..."

pkg install -y python git curl

pip install --upgrade pip
pip install flask ecdsa

echo "✅ Dependências instaladas."

while true; do
  echo ""
  echo "==== Tiburcio Blockchain ===="
  echo "1) Criar carteira"
  echo "2) Minerar (com backup automático)"
  echo "3) Transferir tokens"
  echo "4) Iniciar API (app.py)"
  echo "5) Iniciar P2P"
  echo "6) Consultar saldo"
  echo "7) Sair"
  read -p "Escolha uma opção: " opcao

  case $opcao in
    1)
      echo "🔑 Criando carteira..."
      python3 gerar_carteira.py
      ;;
    2)
      read -p "Digite seu endereço público para receber recompensas: " endereco
      while true; do
        python3 minerador.py << EOF
$endereco
EOF
        cp blockchain.json blockchain_backup_$(date +%Y%m%d%H%M%S).json
        echo "💾 Backup realizado."
        sleep 2
      done
      ;;
    3)
      read -p "Digite seu endereço público (de): " de
      read -p "Digite sua chave privada: " chave_privada
      read -p "Digite o endereço do destinatário (para): " para
      read -p "Digite a quantidade a transferir: " quantidade
      python3 send_tx.py --de "$de" --chave_privada "$chave_privada" --para "$para" --quantidade "$quantidade"
      ;;
    4)
      echo "🚀 Iniciando servidor API em http://localhost:8082 ..."
      python3 app.py
      ;;
    5)
      echo "🌐 Iniciando servidor P2P na porta 5001 ..."
      python3 p2p_server.py
      ;;
    6)
      read -p "Digite o endereço público para consultar saldo: " endereco_saldo
      curl http://localhost:8082/saldo/$endereco_saldo
      ;;
    7)
      echo "👋 Saindo..."
      break
      ;;
    *)
      echo "⚠️ Opção inválida. Tente novamente."
      ;;
  esac
done
