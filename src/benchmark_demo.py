#!/usr/bin/python3
from benchmark import run_benchmark
from benchmark import print_results
import unit_preference_methods
from splitting_methods import first_choice
from splitting_methods import random_choice
from splitting_methods import two_clause_choice

results = run_benchmark(100, 3, 6, 0.2, 5, 1,
                        [unit_preference_methods.random_choice],
                        [two_clause_choice])

print_results(results)
