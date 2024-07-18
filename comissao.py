import sys
import getopt

FEASIBILITY_CUT = False
OPTIMALITY_CUT = False

# Analisa entrada do usuário para ver se os cortes de
# viabilidade e otimalidade estão ativos ou não
def setup_cuts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "fo")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for o in opts:
        global FEASIBILITY_CUT, OPTIMALITY_CUT
        if o == "-f":
            FEASIBILITY_CUT = True
        elif o == "-o":
            OPTIMALITY_CUT = True

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
    print(f"C: {candidates}")

    return S, candidates

def profit(X):
    return len(X)

def Bdada(E, S):
    covered_groups = set().union(*E)
    if covered_groups == S:
        return len(E)
    else:
        return len(E) + 1

def branch_and_bound(E, F, S, OptP, OptX):
    if set().union(*E) == S:
        current_profit = profit(E)
        if current_profit < OptP[0]:
            OptP[0] = current_profit
            OptX[0] = E[:]
    else:
        for x in F:
            newE = E + [x]
            newF = F[F.index(x) + 1:]
            if FEASIBILITY_CUT or Bdada(newE, S) < OptP[0]:
                branch_and_bound(newE, newF, S, OptP, OptX)

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
