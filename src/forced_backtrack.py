#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import first_choice
from splitting_methods import random_choice
from splitting_methods import two_clause_choice
import unit_preference_methods

instance = Instance()

problem = "a \n -d \n b -c \n -b c \n c b d"
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
sol = solve(instance, assignment, two_clause_choice,
            unit_preference_methods.random_choice, True)
print(sol)
