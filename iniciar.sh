#!/bin/bash
# Script para rodar o projeto oficina-programacao-jogos

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

GODOT_EXECUTAVEL=$(find godot -maxdepth 1 -type f ! -name '.*' | sort | head -n 1)

if [ -n "$GODOT_EXECUTAVEL" ]; then
    chmod +x "$GODOT_EXECUTAVEL"
else
    echo "Aviso: nenhum arquivo encontrado em godot/."
    echo "Baixe o executável da Godot e coloque-o na pasta godot/."
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Código específico para subir API do Code Farm
pip install -r jogos/godot-code-farm/code-farm-main/api/requirements.txt

API_DIR="jogos/godot-code-farm/code-farm-main/api/API"
API_LOG="code-farm-api.log"
ROOT_DIR="$PWD"

if [ -d "$API_DIR" ]; then
    (
        cd "$API_DIR" || exit 1
        python -m uvicorn main:app --reload > "$ROOT_DIR/$API_LOG" 2>&1 &
    )
    echo "API do Code Farm iniciada em background. Logs: $API_LOG"
else
    echo "Aviso: diretório da API não encontrado em $API_DIR"
fi

python oficina.py