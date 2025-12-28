import random
import sys


def sgn():
    return random.choice(["", "~"])


def generate_test_case(num_vars, num_clauses, num_soft_clauses, max_weight, filename):
    variables = [f'X{i}' for i in range(1, num_vars + 1)]
    hard_clauses = [set() for i in range(num_clauses)]
    soft_clauses = [set() for i in range(num_soft_clauses)]

    # Generate hard constraints (CNF clauses)
    for variable in variables:
        clause_idx = random.randint(0, num_clauses - 1)
        hard_clauses[clause_idx].add(sgn() + variable)

    for i in range(num_clauses):
        clause_size = random.randint(1, 15)
        for _ in range(clause_size):
            hard_clauses[i].add(sgn() + random.choice(variables))

    # Generate soft constraints (clauses that can be violated)
    for i in range(num_soft_clauses):
        clause_size = random.randint(1, 15)
        for _ in range(clause_size):
            soft_clauses[i].add(sgn() + random.choice(variables))
    # Write to file
    with open(filename, 'w') as f:
        f.write(f'{num_vars} {num_clauses} {
                num_soft_clauses}\n')

        for clause in hard_clauses:
            f.write(f'{" ".join(clause)}\n')

        for clause in soft_clauses:
            f.write(f'SOFT_CLAUSE {" ".join(clause)} {
                    random.randint(1, max_weight)}\n')

    print(f"Test case generated and saved as {filename}")


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python3 test_case_generator.py <num_vars> <num_clauses> <num_soft_clauses> <max_weight> <test_file>")
        sys.exit(1)

    num_vars = int(sys.argv[1])
    num_clauses = int(sys.argv[2])
    num_soft_clauses = int(sys.argv[3])
    max_weight = int(sys.argv[4])
    test_file = sys.argv[5]

    generate_test_case(num_vars, num_clauses,
                       num_soft_clauses, max_weight, test_file)
