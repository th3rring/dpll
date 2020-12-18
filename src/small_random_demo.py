#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import first_choice
from splitting_methods import random_choice
from splitting_methods import two_clause_choice
import random_model
import unit_preference_methods

from utils import Timer
from collections import defaultdict

# heuristics = [two_clause_choice]
heuristics = [first_choice, random_choice, two_clause_choice]

n = 150
rand_problem = random_model.generate_random_problem(n, 3 * n)
print(rand_problem)

rand_instance = Instance()
rand_instance.parse_problem(rand_problem)
rand_instance.setup_watchlist()
rand_assignment = [None] * len(rand_instance.variables)

timer = Timer()
times = defaultdict(list)

for i in range(0, 5):
    print("-----STARTING RUN {}-----".format(i))
    for heuristic in heuristics:
        rand_instance = Instance()
        rand_instance.parse_problem(rand_problem)
        rand_instance.setup_watchlist()
        rand_assignment = [None] * len(rand_instance.variables)

        timer.start()
        sol = solve(rand_instance, rand_assignment, heuristic,
                    unit_preference_methods.random_choice, False)
        tot_time = timer.stop()
        print(f"Elapsed time: {tot_time:0.4f} seconds")

        times[heuristic].append(tot_time)

        print(sol)
        if sol != "UNSAT":
            print("Solution SAT: {}".format(
                rand_instance.check_assignment(rand_assignment)))

for i in range(0, len(heuristics)):
    print("Heuristic {} times: {}".format(i, times[heuristics[i]]))
