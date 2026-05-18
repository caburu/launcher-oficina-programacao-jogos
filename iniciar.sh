#!/bin/bash
# Script para rodar o projeto oficina-programacao-jogos

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

GODOT_EXECUTAVEL=$(find godot -maxdepth 1 -type f | head -n 1)

if [ -n "$GODOT_EXECUTAVEL" ]; then
    chmod +x "$GODOT_EXECUTAVEL"
else
    echo "Aviso: nenhum arquivo encontrado em godot/."
    echo "Baixe o executável da Godot e coloque-o na pasta godot/."
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python oficina.py