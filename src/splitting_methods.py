import operator
from collections import defaultdict
from random import randrange
import random_model


def first_choice(instance, to_attempt, assignment):
    return 0


def random_choice(instance, to_attempt, assignment):
    return randrange(0, len(to_attempt))


def count_unassigned_occurances(instance):
    # Init counting dictionary.
    counts = defaultdict(int)

    # Look at each clause in this problem instance.
    for clause in instance.unassigned_clauses:
        # Get a set of unique unassigned literals.
        unique_vars = set(clause.unassigned)
        for var in unique_vars:
            counts[var] += 1
    return counts


def max_choice(instance, to_attempt, assignment):

    # Update clauses.
    # instance.update_assignment(assignment)

    # Get a count of all unassigned variables.
    counts = count_unassigned_occurances(instance)

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

    if max_occuring_vars:

        # If we have a max occuring variable.
        rand_index = randrange(0, len(max_occuring_vars))
        return to_attempt.index(max_occuring_vars[rand_index])

    else:
        return randrange(0, len(to_attempt))


def vars_in_min_clauses(instance):

    # Use a set here to ensure we don't have duplicates.
    min_clause_vars = set()
    min_clause_len = float("inf")

    for clause in instance.clauses:
        unique_vars = set(clause.unassigned)

        # If this clause has a smaller length, update min.
        if len(unique_vars) < min_clause_len:
            min_clause_vars = unique_vars
            min_clause_len = len(unique_vars)
        # If this clause has the same length as the smallest.
        elif len(unique_vars) == min_clause_len:
            min_clause_vars |= unique_vars

    return list(min_clause_vars)


def moms_choice(instance, to_attempt, assignment):

    # Update clauses.
    instance.update_assignment(assignment)

    # Get a list of all variables in minimum clause length.
    min_clause_vars = vars_in_min_clauses(instance)

    if min_clause_vars:

        # If we have vars that occur in min length clauses.
        rand_index = randrange(0, len(min_clause_vars))
        return to_attempt.index(min_clause_vars[rand_index])

    else:
        return randrange(0, len(to_attempt))


def mams_choice(instance, to_attempt, assignment):

    # Update clauses.
    # instance.update_assignment(assignment)

    # Get a list of all variables in minimum clause length.
    min_clause_vars = vars_in_min_clauses(instance)

    # Get a count of all unassigned variables.
    counts = count_unassigned_occurances(instance)

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

    both_occur = list(set(min_clause_vars) & set(max_occuring_vars))

    if both_occur:
        rand_index = randrange(0, len(both_occur))
        return to_attempt.index(both_occur[rand_index])
    else:
        return randrange(0, len(to_attempt))


def vsid_choice(instance, to_attempt, assignment):

    max_vsid_var_idxs = []
    max_vsid = -float("inf")

    for i in range(len(to_attempt)):

        var = to_attempt[i]

        # If this var has more counts, update maximum.
        if instance.vsid[var] > max_vsid:
            max_vsid_var_idxs = [i]
            max_vsid = instance.vsid[var]
        # If this var has same as max counts, add to list.
        elif instance.vsid[var] == max_vsid:
            max_vsid_var_idxs.append(i)

    if max_vsid_var_idxs:
        rand_index = randrange(0, len(max_vsid_var_idxs))
        return max_vsid_var_idxs[rand_index]
    else:
        return randrange(0, len(to_attempt))


def compute_jeroslow_wang(instance, var):
    ret = 0
    for clause in instance.unassigned_clauses:
        if var in clause.unassigned:
            ret += 2**(-len(clause.unassigned))
    return ret


def compute_jeroslow_wang_literal(instance, var, negated):
    ret = 0
    for clause in instance.unassigned_clauses:

        # Check if this literal is in this clause.
        if var in clause.unassigned and negated == clause.get_literal_from_var(
                var).negated:
            ret += 2**(-len(set(clause.unassigned)))
    return ret


def jeroslow_wang_choice(instance, to_attempt, assignment):

    # Assuming instance has been updated already.

    # Init variables for max search.
    max_j_var_idx = None
    max_j = -float("inf")

    for i in range(len(to_attempt)):

        # Compute the j value for this var.
        j = compute_jeroslow_wang(instance, to_attempt[i])

        # Check if this value is larger.
        if j > max_j:
            max_j_var_idx = i
            max_j = j

    return max_j_var_idx


def jeroslow_wang_literal_choice(instance, to_attempt, assignment):

    # Assuming instance has been updated already.

    # Init variables for max search.
    max_j_var_idx = None
    max_j = -float("inf")

    for i in range(len(to_attempt)):
        for negated in [False, True]:

            # Compute the j value for this literal.
            j = compute_jeroslow_wang_literal(instance, to_attempt[i], negated)

            # Check if this value is larger.
            if j > max_j:
                max_j_var_idx = i
                max_j = j

    return max_j_var_idx


def two_clause_choice(instance, to_attempt, assignment):

    # Update the n_clauses mapping.
    # instance.update_assignment(assignment)

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
