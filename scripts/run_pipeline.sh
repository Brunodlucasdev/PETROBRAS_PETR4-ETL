#!/bin/bash

echo "Iniciando o Pipeline de Dados..."

# Navega para a pasta raiz do projeto considerando o local do script
cd "$(dirname "$0")/.."

# Ativa o ambiente virtual
source venv/bin/activate

# Executa o script de extração
python scripts/extract_data.py

# Desativa o ambiente virtual
deactivate

echo "Pipeline finalizado com sucesso!"