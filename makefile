# Nome do arquivo Python
PYTHON_FILE=comissao.py

# Nome do executável gerado
EXECUTABLE=comissao

# Caminho do PyInstaller
PYINSTALLER=pyinstaller

# Diretório de saída
DIST_DIR=dist

# Alvo padrão
all: build

# Alvo para construir o executável
build:
	$(PYINSTALLER) --onefile $(PYTHON_FILE)

# Alvo para limpar arquivos gerados
clean:
	rm -rf $(DIST_DIR) $(EXECUTABLE).spec build

.PHONY: all build clean
