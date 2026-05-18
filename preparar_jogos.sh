#!/bin/bash
# Script para preparar os jogos para a oficina
# Remove histórico git antigo e reinicia o controle de versão em cada subpasta de jogos/

JOGOS_DIR="jogos"

if [ ! -d "$JOGOS_DIR" ]; then
  echo "Diretório '$JOGOS_DIR' não encontrado. Execute este script na raiz do projeto."
  exit 1
fi

for jogo in "$JOGOS_DIR"/*; do
  if [ -d "$jogo" ]; then
    if [ -d "$jogo/.git" ]; then
      echo "Removendo histórico git antigo de $jogo..."
      rm -rf "$jogo/.git"
    fi
    echo "Inicializando novo repositório git em $jogo..."
    (cd "$jogo" && git init -q && git add . && git commit -q -m "Versão base para oficina")
  fi
  done

echo "Jogos preparados para a oficina. Cada pasta agora tem um repositório git limpo para restauração."