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
    
    print(f"CORTE VIABILIDADE: {FEASIBILITY_CUT}")
    print(f"CORTE OTIMALIDADE: {OPTIMALITY_CUT}")
    print(f"GUIVEN_B: {GUIVEN_B}")

# Lê entrada do usuário para guardar informações
# sobre os grupos (S) e candidatos (candidates)
def read_input():
    data = input_data = sys.stdin.read().strip().split()

    index = 0
    l = int(data[index])
    index = 1
    n = int(data[index])
    index += 1

    S = set(range(1, l + 1))
    candidates = []

    print(f"l: {l} n:{n}")
    for i in range(n):
        candidate = []
        candidate_rep = int(data[index])
        index += 1 
        for j in range(candidate_rep):
            candidate.append(int(data[index]))
            index += 1
        candidates.append(candidate)

    #Debug
    print(f"S: {S}")
    print(f"F: {candidates}")

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

# Nossa função limitante
def B_difference(E, S):
    #print("Nossa versão! [diferença]")
    groups_represented = make_union(E)
    remaining_groups = S - groups_represented
    if not remaining_groups:
        return len(E)
    return len(E) + len(remaining_groups)

def B_proportion(E, S):
    #print("Nossa versão! [proporção]")
    covered_groups = make_union(E)
    remaining_groups = S - covered_groups
    if not remaining_groups:
        return len(E)
    proportion_remaining = len(remaining_groups) / len(S)
    return len(E) + int(proportion_remaining * len(S))


def B_min_candidate(E, S, F):
    covered_groups = make_union(E)
    remaining_groups = S - covered_groups
    if not remaining_groups:
        return len(E)
    max_coverage = 0
    for f in F:
        coverage = len(set(f) & remaining_groups)
        if coverage > max_coverage:
            max_coverage = coverage
    if max_coverage == 0:  # Evitar divisão por zero
        estimated_additional_candidates = len(remaining_groups)
    else:
        estimated_additional_candidates = (len(remaining_groups) + max_coverage - 1) // max_coverage
    return len(E) + estimated_additional_candidates

def B_coverage_gap(E, S, F):
    covered_groups = make_union(E)  # Grupos já cobertos pelos amigos convidados
    remaining_groups = S - covered_groups  # Grupos que ainda precisam ser cobertos
    
    if not remaining_groups:  # Se não houver grupos restantes, todos estão cobertos
        return len(E)
    
    # Calcular o número médio de grupos que os amigos restantes podem cobrir
    average_coverage = sum(len(set(f) & remaining_groups) for f in F) / len(F)
    
    if average_coverage == 0:  # Evitar divisão por zero
        estimated_additional_friends = len(remaining_groups)
    else:
        estimated_additional_friends = (len(remaining_groups) / average_coverage)
    
    # Retornar o número atual de amigos + a estimativa de amigos adicionais necessários
    return len(E) + estimated_additional_friends


def B_average(E, S):
    #print("Nossa versão! [média]")
    covered_groups = make_union(E)
    remaining_groups = S - covered_groups
    if not remaining_groups:
        return len(E)
    if E:
        average_coverage = len(covered_groups) / len(E)
    else:
        average_coverage = 1  # Evitar divisão por zero no início
    estimated_additional_candidates = len(remaining_groups) / average_coverage
    return len(E) + int(estimated_additional_candidates)

# Função de gerenciamento entre versões de função limitante
def set_B(E,S, F):
    if GUIVEN_B:
        #print("Versão do professor!")
        return B_simple(E,S)
    else:
        return B_difference(E,S, F)

def branch_and_bound(E, F, S, OptP, OptX):
    # print(f"E:[{make_union(E)}] == S:[{S}] ? {make_union(E) == S}")
    global COUNT 
    COUNT += 1
    if (FEASIBILITY_CUT and make_union(E) == S):
        current_profit = profit(E)
        # print(f"current_profit: {current_profit} < OptP[0]: {OptP[0]} ?")
        # print(f"antigo OptP[0]: [{OptP[0]}]")
        # print(f"antigo OptX[0]: [{OptX[0]}]")
        if current_profit < OptP[0]:
            OptP[0] = current_profit
            OptX[0] = E[:]
            # print(f"novo OptP[0]: [{OptP[0]}]")
            # print(f"novo OptX[0]: [{OptX[0]}]")
    else:
        # print("entrou no else")
        # print(f"antigo E: [{E}]")
        # print(f"antigo F: [{F}]")
        for x in F:
            # print(f"Estamos analisando {x} dentre F:[{F}]")
            new_E = E + [x] 
            new_F = F[F.index(x) + 1:]
            # print(f"novo E: [{new_E}]")
            # print(f"novo F: [{new_F}]")
            if (OPTIMALITY_CUT and set_B(new_E, S, new_F) < OptP[0]):
                # print(f"B: {set_B(new_E, S, F)} < OptP[0]: {OptP[0]} ? {set_B(new_E, S, F) < OptP[0]}")
                if set_B(new_E, S, F) < OptP[0]:
                    branch_and_bound(new_E, new_F, S, OptP, OptX)


# FUnção wrapper pro Branch&Bound
def minimum_representative(S, candidates):
    OptP = [float('inf')]
    OptX = [[]]
    E = []
    F = candidates
    start_time = time.time()
    branch_and_bound(E, F, S, OptP, OptX)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Levou: {format(total_time, '.2e')} segundos")
    print(f"Nós percorridos: {COUNT}")
    if OptP[0] == float('inf'):
        return "Inviavel"
    else:
        return OptX[0]

def main():
    setup_cuts()
    S, candidates = read_input()
    result = minimum_representative(S, candidates)
    if result == "Inviavel":
        print(result)
    else:
        indices = [candidates.index(groups) + 1 for groups in result]
        indices.sort()
        print(" ".join(map(str, indices)))

if __name__ == "__main__":
    main()
