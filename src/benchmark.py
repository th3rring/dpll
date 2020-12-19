from instance import Instance
from sat import solve
import random_model

from utils import Timer
from collections import defaultdict
import concurrent.futures
import numpy as np

# A time of -1 marks a timeout!


def run_benchmark(n, ratio_min, ratio_max, ratio_step, timeout_seconds,
                  num_experiments, unit_preference_heuristics,
                  splitting_heuristics):

    # Result dictionary has keys: ratio, unit preference heuristic, splitting heuristic.
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Create a new timer.
    timer = Timer()

    for ratio in np.arange(ratio_min, ratio_max + ratio_step, ratio_step):

        # Calculate the number of clauses for this n.
        l = int(ratio * n)

        # Repeat num_experiment runs with this ratio.
        for _ in range(num_experiments):

            # Generate a random model to test.
            problem = random_model.generate_random_problem(n, l)

            # Iterate over all heuristics.
            for up in unit_preference_heuristics:
                for split in splitting_heuristics:

                    instance = Instance()
                    instance.parse_problem(problem)
                    instance.setup_watchlist()

                    assignments = [None] * len(instance.variables)

                    # Init result variables.
                    solution = None
                    num_calls = None
                    solve_timeout = False

                    timer.start()

                    # Start another thread to attempt solving.
                    with concurrent.futures.ThreadPoolExecutor(
                            max_workers=1) as executor:

                        # Create a worker thread.
                        future = executor.submit(solve, instance, assignments,
                                                 split, up, False)

                        # Catch if this times out.
                        try:
                            solution, num_calls = future.result(
                                timeout=timeout_seconds)
                        except concurrent.futures.TimeoutError:
                            solve_timeout = True
                            timer.stop()

                    if solve_timeout:
                        solve_time = "TIMEOUT"
                        num_calls = -1
                        solution = "UNSAT"
                    else:
                        solve_time = timer.stop()

                    # Add result of this run to the results dictionary.
                    results[ratio][up.__name__][split.__name__].append(
                        (solve_time, num_calls, solution != "UNSAT"))
    return results


def print_results(results):

    print("----RESULTS----")

    for ratio in results:
        print("Ratio: {}".format(ratio))
        for up in results[ratio]:
            for split in results[ratio][up]:
                print("   Unit Pref: {}, Splitting: {}:".format(up, split))
                for exps in results[ratio][up][split]:
                    print("      {}".format(exps))
