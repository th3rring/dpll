#!/usr/bin/python3
from benchmark import run_benchmark
from benchmark import print_results
from unit_preference_methods import *
from splitting_methods import *

results = run_benchmark(100, 3, 4.4, 0.2, 5, 5, [max_unit_choice],
                        [two_clause_choice, jeroslow_wang_choice])

print_results(results)
