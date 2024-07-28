# Variáveis
PYTHON = python3
PIP = pip3
VENV = venv
VENV_BIN = $(VENV)/bin
ACTIVATE = . $(VENV_BIN)/activate
SCRIPT = comissao.py

# Regras
.PHONY: all venv install requirements test lint clean run

all: install

# Cria um ambiente virtual
venv:
	$(PYTHON) -m venv $(VENV)

# Instala as dependências
install: venv
	$(ACTIVATE) && $(PIP) install -r requirements.txt

# Instala as dependências (caso o requirements.txt tenha sido alterado)
requirements: venv
	$(ACTIVATE) && $(PIP) install -r requirements.txt

# Executa os testes
test:
	$(ACTIVATE) && pytest

# Executa o linter
lint:
	$(ACTIVATE) && flake8 $(SCRIPT)

# Limpa arquivos temporários
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf $(VENV)

# Roda o script principal
run:
	$(ACTIVATE) && $(PYTHON) $(SCRIPT)

