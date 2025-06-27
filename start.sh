#!/bin/bash

PORTA_SALDO=5003
PORTA_APP=8082

start_app() {
  echo "Iniciando servidor API app.py na porta $PORTA_APP..."
  nohup python3 app.py > app.log 2>&1 &
  echo "Servidor app.py rodando em background. Log: app.log"
}

start_servidores() {
  echo "Iniciando Full Node sem carteira (apenas full node)..."
  nohup python3 tiburcio_full_node.py > full_node.log 2>&1 &
  echo "Full Node rodando em background. Log: full_node.log"

  echo "Iniciando servidor P2P..."
  nohup python3 p2p_server.py > p2p_server.log 2>&1 &
  echo "Servidor P2P rodando. Log: p2p_server.log"

  echo "Iniciando servidor de saldo na porta $PORTA_SALDO..."
  nohup python3 saldo_server.py > saldo_server.log 2>&1 &
  echo "Servidor de saldo rodando. Log: saldo_server.log"

  start_app
}

minerar() {
  read -p "Digite o endereço da carteira mineradora: " carteira
  if [ -z "$carteira" ]; then
    echo "Você precisa fornecer uma carteira para minerar."
    return
  fi
  echo "Iniciando minerador para carteira: $carteira"
  python3 minerador.py --minerador "$carteira"
}

enviar_transacao() {
  echo "Executando envio de transação assinada online..."
  read -p "Endereço público (de): " sender
  read -p "Chave privada (hex): " chave_privada
  read -p "Endereço do destinatário (para): " recipient
  read -p "Quantidade a transferir: " quantidade

  python3 send_tx.py "$sender" "$chave_privada" "$recipient" "$quantidade"

  echo "Transação enviada. Voltando ao menu..."
  sleep 2
}

consultar_saldo() {
  read -p "Digite o endereço público para consultar saldo: " endereco
  curl http://localhost:$PORTA_SALDO/saldo/$endereco
  echo
}

consolidar_blocos() {
  echo "Consolidando blocos..."
  python3 consolidar_blockchain.py
}

parar_tudo() {
  echo "Parando todos os processos..."
  pkill -f tiburcio_full_node.py
  pkill -f p2p_server.py
  pkill -f saldo_server.py
  pkill -f minerador.py
  pkill -f app.py
  echo "Todos os servidores foram encerrados."
}

while true; do
  echo
  echo "=== Tiburcio Blockchain - Menu ==="
  echo "1) Iniciar todos os servidores (Full Node + P2P + Saldo + API)"
  echo "2) Minerar (minerador.py)"
  echo "3) Enviar transação"
  echo "4) Consultar saldo"
  echo "5) Consolidar blocos (recuperar saldo)"
  echo "0) Sair"
  read -p "Escolha uma opção: " opcao

  case $opcao in
    1) start_servidores ;;
    2) minerar ;;
    3) enviar_transacao ;;
    4) consultar_saldo ;;
    5) consolidar_blocos ;;
    0) echo "Saindo..."; exit 0 ;;
    *) echo "Opção inválida!" ;;
  esac
done
