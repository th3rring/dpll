from random import randrange
from collections import defaultdict


def random_unit_choice(instance):
    return randrange(0, len(instance.n_clauses[1]))


def max_unit_choice(instance):

    unit_clauses = instance.n_clauses[1]

    # Init dictionary of unit clause indexes per variable.
    clauses = defaultdict(list)

    # Look at each clause in this problem instance.
    for i in range(len(unit_clauses)):

        # Add this unit clause to dict with variable key.
        clauses[unit_clauses[i].unassigned[0]].append(i)

    # Find the variables that occur in the max number of unit props.
    max_occuring_vars = []
    max_count = -float("inf")

    for var in clauses:

        count = len(clauses[var])

        # If this var has more counts, update maximum.
        if count > max_count:
            max_occuring_vars = [var]
            max_count = count
        # If this var has same as max counts, add to list.
        elif count == max_count:
            max_occuring_vars.append(var)

    if max_occuring_vars:

        # Find a random variable that occurs in max number of unit props.
        rand_var_idx = randrange(0, len(max_occuring_vars))
        var_max = max_occuring_vars[rand_var_idx]

        # Find a random clause that the variable occurs in.
        rand_prop_idx = randrange(0, len(clauses[var_max]))
        return clauses[var_max][rand_prop_idx]

    else:
        return randrange(0, len(unit_clauses))
