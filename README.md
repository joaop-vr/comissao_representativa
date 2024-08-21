# Projeto de Cálculo de Comissões - Otimização

Este repositório contém a implementação do algoritmo de Branch & Bound para resolver o problema da **Comissão Representativa**. Este projeto foi desenvolvido como parte da disciplina de **Otimização** na Universidade Federal do Paraná (UFPR), durante o primeiro semestre de 2024.

## Descrição do Problema

O problema consiste em selecionar um subconjunto mínimo de candidatos para formar uma comissão representativa, de forma que todos os grupos da sociedade estejam representados. O objetivo é encontrar o menor número de candidatos que representem todos os grupos.

### Detalhes

- **Entrada**: Conjuntos de candidatos e grupos sociais, onde cada candidato pode pertencer a um ou mais grupos.
- **Saída**: O menor conjunto de candidatos que representa todos os grupos ou a indicação de que é impossível formar tal comissão.

## Implementação

O algoritmo foi implementado utilizando a técnica de Branch & Bound, uma abordagem clássica em problemas de otimização combinatória. Além disso, o projeto inclui:

- **Modelagem do problema**: A definição formal do problema e a explicação de como ele foi modelado para ser resolvido pelo algoritmo de Branch & Bound.
- **Funções limitantes**: Duas funções limitantes foram implementadas:
  1. **Função dada pelo professor**: Usada para comparar com a função proposta pelos alunos.
  2. **Função proposta pelos alunos**: Utilizada como padrão na implementação, busca ser mais eficiente que a função fornecida.

## Arquivos no Repositório

- `comissao.py`: Implementação do algoritmo de Branch & Bound para o problema da Comissão Representativa.
- `script_testes.py`: Script para testar o funcionamento correto do algoritmo com diferentes cenários de entrada.
- `testes/`: Pasta contendo arquivos de entrada para testar diferentes casos do problema.

## Como Usar

### Execução

1. Para executar o algoritmo de Branch & Bound com a função limitante padrão:
    ```bash
    python comissao.py
    ```

2. Para executar o algoritmo desativando cortes de viabilidade:
    ```bash
    python comissao.py -f
    ```

3. Para executar o algoritmo desativando cortes de otimalidade:
    ```bash
    python comissao.py -o
    ```

4. Para utilizar a função limitante fornecida pelo professor:
    ```bash
    python comissao.py -a
    ```

### Testes

Para executar os testes que validam o comportamento do algoritmo:
```bash
python script_testes.py
