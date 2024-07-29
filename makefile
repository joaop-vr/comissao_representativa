# Define o interpretador para o Makefile
SHELL := /bin/bash

# Nome do script Python
SCRIPT = comissao.py

# Alvo padrão
all: run

# Alvo para rodar o script
run:
	@chmod +x $(SCRIPT)
	@./$(SCRIPT)

# Alvo para limpar arquivos gerados (se aplicável)
clean:
	@echo "Nada para limpar no momento."
