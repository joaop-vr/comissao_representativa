import sys
import getopt
import time
import os

GUIVEN_B = False
FEASIBILITY_CUT = True
OPTIMALITY_CUT = True
COUNT = 0
FUNCS = []
ITERATOR = 0

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

def read_input(input_data):
    data = input_data.strip().split()

    index = 0
    l = int(data[index])
    index += 1
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

    # Debug
    print(f"S: {S}")
    print(f"F: {candidates}")

    return S, candidates

def profit(X):
    return len(X)

def make_union(E):
    output = set()
    for group in E:
        output.update(group)
    return output

def B_simple(E, S):
    if make_union(E) == S:
        return len(E)
    else:
        return len(E) + 1

def B_difference(E, S):
    groups_represented = make_union(E)
    remaining_groups = S - groups_represented
    if not remaining_groups:
        return len(E)
    return len(E) + len(remaining_groups)

def B_proportion(E, S):
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

def B_average(E, S):
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

def set_B(E, S, F):
    func_B = FUNCS[ITERATOR]
    if func_B == B_min_candidate:
        return func_B(E, S, F)
    else:
        return func_B(E, S)

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


def minimum_representative(S, candidates):
    global FUNCS, ITERATOR, COUNT
    FUNCS = [B_simple, B_difference, B_proportion, B_min_candidate, B_average]
    results = []

    for i in range(len(FUNCS)):
        OptP = [float('inf')]
        OptX = [[]]
        E = []
        F = candidates
        ITERATOR = i
        # if FUNCS[ITERATOR] == B_simple:
        #     print("Versão do professor!")
        # elif FUNCS[ITERATOR] == B_difference:
        #     print("Versão da Diferença!")
        # elif FUNCS[ITERATOR] == B_proportion:
        #     print("Versão Proporcional!")
        # elif FUNCS[ITERATOR] == B_min_candidate:
        #     print("Versão Mínimo Candidato!")
        # elif FUNCS[ITERATOR] == B_average:
        #     print("Versão Média!")
        start_time = time.time()
        branch_and_bound(E, F, S, OptP, OptX)
        end_time = time.time()
        total_time = end_time - start_time
        # print(f"Levou: {format(total_time, '.2e')} segundos")
        # print(f"Nós percorridos: {COUNT}")
        results.append((OptP[0], OptX[0], COUNT, total_time))
        COUNT = 0

    return results

def process_test_file(file_path):
    with open(file_path, 'r') as file:
        input_data = file.read()
    S, candidates = read_input(input_data)
    results = minimum_representative(S, candidates)
    for i, (opt_p, opt_x, count, total_time) in enumerate(results):
        if opt_p == float('inf'):
            print(f"Função {FUNCS[i].__name__}: Inviável")
        else:
            indices = [candidates.index(groups) + 1 for groups in opt_x]
            indices.sort()
            print(f"Função {FUNCS[i].__name__}: {opt_p} candidatos, {count} nós percorridos, {format(total_time, '.2e')} segundos")
            print(f"Candidatos: {' '.join(map(str, indices))}")

def main():
    setup_cuts()
    test_dir = "testes"
    for test_file in os.listdir(test_dir):
        if test_file.endswith(".txt"):
            file_path = os.path.join(test_dir, test_file)
            print(f"\n\nProcesando {file_path}...")
            process_test_file(file_path)

if __name__ == "__main__":
    main()
