from random import randrange


def generate_random_problem(n, l):

    # Start with empty string.
    prob = ""

    # Generate each clause.
    for _ in range(0, l):
        cur_string = ""

        # We are generating 3-SAT problems.
        for _ in range(0, 3):

            # Choost a variable and negate it randomly.
            var = randrange(0, n)
            negated = "-" if randrange(0, 2) == 1 else ""
            cur_string += "{}x{} ".format(negated, var)

        # Add this clause to the overall problem.
        cur_string += "\n "
        prob += cur_string

    # Return and remove last new line.
    return prob[:-3]
