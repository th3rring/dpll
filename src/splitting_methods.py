import operator
from collections import defaultdict
from random import randrange
import random_model

first_choice = lambda instance, to_attempt, assignment: 0
random_choice = lambda instance, to_attempt, assignment: randrange(
    0, len(to_attempt))


def two_clause_choice(instance, to_attempt, assignment):
    # print("--TWO CHOICE--")
    # print("  to_attempt: {}".format(to_attempt))
    # print("  assignment: {}".format(assignment))
    counts = defaultdict(int)

    for index in range(0, len(to_attempt)):
        var = to_attempt[index]
        for clause in instance.clauses:
            if var in clause and clause.count_unassigned(assignment) == 2:
                counts[index] += 1

    # print("  counts: {}".format(counts))

    # No variables exist in 2-clauses, use random.
    if not counts.items():
        ret_val = randrange(0, len(to_attempt))
    else:
        ret_val = max(counts.items(), key=operator.itemgetter(1))[0]

    # print("  returned: %i" % ret_val)
    return ret_val
