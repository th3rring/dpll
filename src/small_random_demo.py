#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import first_choice
from splitting_methods import random_choice
from splitting_methods import two_clause_choice
import random_model

n = 20
rand_problem = random_model.generate_random_problem(n, 3 * n)

rand_instance = Instance()
rand_instance.parse_problem(rand_problem)
rand_instance.setup_watchlist()
rand_assignment = [None] * len(rand_instance.variables)

# results = solve(rand_instance, rand_assignment, random_choice)
# solutions = set()
# for result in results:
#     solutions.add(str(result))

# for sol in solutions:
#     print(sol)
for heuristic in [first_choice, random_choice, two_clause_choice]:
    rand_instance = Instance()
    rand_instance.parse_problem(rand_problem)
    rand_instance.setup_watchlist()
    rand_assignment = [None] * len(rand_instance.variables)
    sol = solve(rand_instance, rand_assignment, heuristic, False)
    print(sol)
    print("Solution SAT: {}".format(
        rand_instance.check_assignment(rand_assignment)))
