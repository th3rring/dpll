import operator
from collections import defaultdict
from random import randrange
import random_model

first_choice = lambda instance, to_attempt, assignment: 0
random_choice = lambda instance, to_attempt, assignment: randrange(
    0, len(to_attempt))


def two_clause_choice(instance, to_attempt, assignment):

    # Update the n_clauses mapping.
    instance.update_assignment(assignment)

    # Get all unsat 2-clauses.
    two_clauses = instance.n_clauses[2]

    # No variables exist in 2-clauses, use random.
    if not two_clauses:
        return randrange(0, len(to_attempt))
    else:

        # Init counting dictionary.
        counts = defaultdict(int)

        # For each clause, add one to variables occuring.
        for clause in instance.n_clauses[2]:

            # Ensure that we have unique variables
            unique_vars = set(clause.unassigned)
            for var in unique_vars:
                counts[var] += 1

        max_occuring_vars = []
        max_count = -float("inf")

        for var in counts:

            # If this var has more counts, update maximum.
            if counts[var] > max_count:
                max_occuring_vars = [var]
                max_count = counts[var]
            # If this var has same as max counts, add to list.
            elif counts[var] == max_count:
                max_occuring_vars.append(var)

        # Choose a random variable that has max number of 2-clause occurances.
        rand_index = randrange(0, len(max_occuring_vars))
        return to_attempt.index(max_occuring_vars[rand_index])
