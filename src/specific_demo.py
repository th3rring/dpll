#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import *
import random_model
from unit_preference_methods import *

from utils import Timer
from collections import defaultdict

heuristics = [first_choice]
# heuristics = [first_choice, random_choice, two_clause_choice]

n = 5
rand_problem = """-x4 x3 -x2
 x2 x0 x2
 -x2 -x4 -x2
 x3 -x4 x1
 -x0 x1 x1
 x2 -x4 x3
 x1 x2 x1
 x3 -x2 -x1
 -x0 -x4 -x4
 x0 x3 x2
 x1 x1 x0
 x1 -x0 -x2
 x3 x1 x2
 -x2 -x1 -x3
 -x1 -x0 x0"""
print(rand_problem)

rand_instance = Instance()
rand_instance.parse_problem(rand_problem)
rand_instance.setup_watchlist()
rand_assignment = [None] * len(rand_instance.variables)

timer = Timer()
times = defaultdict(list)

for i in range(0, 1):
    print("-----STARTING RUN {}-----".format(i))
    for heuristic in heuristics:
        rand_instance = Instance()
        rand_instance.parse_problem(rand_problem)
        rand_instance.setup_watchlist()
        rand_assignment = [None] * len(rand_instance.variables)

        timer.start()
        sol = solve(rand_instance, rand_assignment, heuristic,
                    random_unit_choice, True)
        tot_time = timer.stop()
        print(f"Elapsed time: {tot_time:0.4f} seconds")

        times[heuristic].append(tot_time)

        print(sol)
        if sol != "UNSAT":
            print("Solution SAT: {}".format(
                rand_instance.check_assignment(rand_assignment)))

for i in range(0, len(heuristics)):
    print("Heuristic {} times: {}".format(i, times[heuristics[i]]))

# print(rand_instance.variables)
# print("potential {}".format(
#     rand_instance.check_assignment([False, False, False, True, True])))
# print("potential {}".format(
#     rand_instance.check_assignment([False, False, False, False, True])))
