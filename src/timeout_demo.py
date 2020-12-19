#!/usr/bin/python3
from instance import Instance
from sat import solve
from splitting_methods import *
import random_model
from unit_preference_methods import *

from utils import Timer
from collections import defaultdict
import concurrent.futures

n = 150
rand_problem = random_model.generate_random_problem(n, 5 * n)

rand_instance = Instance()
rand_instance.parse_problem(rand_problem)
rand_instance.setup_watchlist()
rand_assignment = [None] * len(rand_instance.variables)

timer = Timer()

timer.start()

print("Starting solve...")

sol = None
calls = None
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future = executor.submit(solve, rand_instance, rand_assignment,
                             two_clause_choice, max_unit_choice, False)
    try:
        sol, calls = future.result(timeout=1)
    except concurrent.futures.TimeoutError:
        print("TIMEOUT!")
        exit()

tot_time = timer.stop()

print("Sat {}, time {}, calls {}".format(sol != "UNSAT", tot_time, calls))
