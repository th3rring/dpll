#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import first_choice
from splitting_methods import random_choice
from splitting_methods import two_clause_choice

instance = Instance()

problem = "x1 x3 -x4 \n x4 \n x2 -x3 \n -x5"
instance.parse_problem(problem)
instance.setup_watchlist()

assignment = [None] * len(instance.variables)
# results = solve(instance, assignment, first_choice)
# solutions = set()
# for result in results:
#     solutions.add(str(result))
#
# for sol in solutions:
#     print(sol)
sol = solve(instance, assignment, first_choice)
print(sol)
