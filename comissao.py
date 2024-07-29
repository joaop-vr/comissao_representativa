#!/usr/bin/env python3
import sys
import getopt
import time

GUIVEN_B = False
FEASIBILITY_CUT = True
OPTIMALITY_CUT = True
COUNT = 0

# Analisa entrada do usuário para ver se os cortes de
# viabilidade e otimalidade estão ativos ou não
def setup_cuts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "afo")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    global FEASIBILITY_CUT, OPTIMALITY_CUT, GUIVEN_B
    for opt, arg in opts:
        if opt == '-f':
            FEASIBILITY_CUT = False
        elif opt == '-o':
            OPTIMALITY_CUT = False
        elif opt == '-a':
            GUIVEN_B = True

# Lê entrada do usuário para guardar informações
# sobre os grupos (S) e candidatos (candidates)
def read_input():
    data = sys.stdin.read().strip().split()

    index = 0
    l = int(data[index])
    index += 1
    n = int(data[index])
    index += 1

    S = set(range(1, l + 1))
    candidates = []

    for i in range(n):
        candidate = []
        candidate_rep = int(data[index])
        index += 1 
        for j in range(candidate_rep):
            candidate.append(int(data[index]))
            index += 1
        candidates.append(candidate)

    return S, candidates

def profit(X):
    return len(X)

# Realiza a união sem repetição dos conjuntos de E
def make_union(E):
    output = set()
    for group in E:
        output.update(group)
    return output

# Função limitante do professor
def B_simple(E, S):
    if make_union(E) == S:
        return len(E)
    else:
        return len(E) + 1

def B_min_candidate(E, S, F):
    covered_groups = make_union(E)
    remaining_groups = S - covered_groups

    if not remaining_groups:
        return len(E)

    # Encontra o maior lucro que podemos obter desse
    # conjunto de candidatos
    max_profit = 0
    for f in F:
        coverage = len(set(f) & remaining_groups)
        if coverage > max_profit:
            max_profit = coverage

    if max_profit == 0: # Evitar divisão por zero
        estimated_additional_candidates = len(remaining_groups)
    else:
        estimated_additional_candidates = (len(remaining_groups) + max_profit - 1) // max_profit # Técnica de arredondamento
    return len(E) + estimated_additional_candidates

# Função de gerenciamento entre versões de função limitante
def set_B(E, S, F):
    if GUIVEN_B:
        return B_simple(E, S)
    else:
        return B_min_candidate(E, S, F)

def branch_and_bound(E, F, S, OptP, OptX):
    global COUNT 
    COUNT += 1
    if make_union(E) == S:
        current_profit = profit(E)
        if current_profit < OptP[0]:
            OptP[0] = current_profit
            OptX[0] = E[:]
    else:
        for x in F:
            new_E = E + [x]
            new_F = F[F.index(x) + 1:]
            limit_value = set_B(new_E, S, new_F)
            if (FEASIBILITY_CUT and limit_value <= OptP[0]) or not FEASIBILITY_CUT:
                if (OPTIMALITY_CUT and limit_value < OptP[0]) or not OPTIMALITY_CUT:
                    branch_and_bound(new_E, new_F, S, OptP, OptX)

# Função wrapper para Branch&Bound
def minimum_group(S, candidates):
    OptP = [float('inf')]
    OptX = [[]]
    E = []
    F = candidates
    start_time = time.time()
    branch_and_bound(E, F, S, OptP, OptX)
    end_time = time.time()
    total_time = end_time - start_time
    # Relatório
    sys.stderr.write(f"{COUNT} {format(total_time, '.2e')}")
    
    if OptP[0] == float('inf'):
        return "Inviavel"
    else:
        return OptX[0]

def main():
    setup_cuts()
    S, candidates = read_input()
    result = minimum_group(S, candidates)
    if result == "Inviavel":
        print(result)
    else:
        indices = [candidates.index(groups) + 1 for groups in result]
        indices.sort()
        print(" ".join(map(str, indices)))

if __name__ == "__main__":
    main()
