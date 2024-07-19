import sys
import getopt

GUIVEN_B = False
FEASIBILITY_CUT = True
OPTIMALITY_CUT = True

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
    groups_represented = make_union(E)
    remaining_groups = S - groups_represented
    if not remaining_groups:
        return len(E)
    return len(E) + len(remaining_groups)

# Função de gerenciamento entre versões de função limitante
def set_B(E,S):
    if GUIVEN_B:
        print("Versão do professor!")
        return B_simple(E,S)
    else:
        print("Nossa versão!")
        return B_difference(E,S)

def branch_and_bound(E, F, S, OptP, OptX):
    print(f"E:[{make_union(E)}] == S:[{S}] ?")
    if make_union(E) == S:
        current_profit = profit(E)
        print(f"current_profit: {current_profit} < OptP[0]: {OptP[0]} ?")
        print(f"antigo OptP[0]: [{OptP[0]}]")
        print(f"antigo OptX[0]: [{OptX[0]}]")
        if current_profit < OptP[0]:
            OptP[0] = current_profit
            OptX[0] = E[:]
            print(f"novo OptP[0]: [{OptP[0]}]")
            print(f"novo OptX[0]: [{OptX[0]}]")
    else:
        print("entrou no else")
        print(f"antigo E: [{E}]")
        print(f"antigo F: [{F}]")
        for x in F:
            print(f"Estamos analisando {x} dentre F:[{F}]")
            new_E = E + F[:F.index(x)+1]
            new_F = F[F.index(x) + 1:]
            print(f"novo E: [{new_E}]")
            print(f"novo F: [{new_F}]")
            #if (FEASIBILITY_CUT or set_B(new_E, S) < OptP[0]) and (OPTIMALITY_CUT or set_B(new_E, S) < OptP[0]):
            print(f"B: {set_B(new_E, S)} < OptP[0]: {OptP[0]} ? {set_B(new_E, S) < OptP[0]}")
            if set_B(new_E, S) < OptP[0]:
                branch_and_bound(new_E, new_F, S, OptP, OptX)

# FUnção wrapper pro Branch&Bound
def minimum_representative(S, candidates):
    OptP = [float('inf')]
    OptX = [[]]
    E = []
    F = candidates
    branch_and_bound(E, F, S, OptP, OptX)
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
