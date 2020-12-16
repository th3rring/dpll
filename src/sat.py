from instance import State
from instance import Literal
from utils import timerDecorator
from utils import Timer


@timerDecorator
def solve(instance, assignment, splitting, verbose):

    n = len(instance.variables)
    state = [State(0)] * n

    to_attempt = list(range(0, n))
    previous_attempts = []

    while True:
        # if d == n:
        #   yield assignment
        #   d -= 1
        #   continue

        if not to_attempt:
            # We return the first sat result we get.
            # Change this line to a yield in order to search for all.
            return assignment

            # Look again at the previously attempted assignment.
            # to_attempt.append(previous_attempts.pop())
            # continue

        # Try the first element of to_attempt.
        idx = splitting(instance, to_attempt, assignment)
        variable_to_try = to_attempt[idx]

        if verbose:
            print("Attempting %i" % variable_to_try)
            print("   to_attempt: {}".format(to_attempt))
            print("   previous_attempts: {}".format(previous_attempts))

        tried_something = False
        found_sat = False

        for a in [False, True]:

            # Check if we can attempt this assignment.
            if State.can_try(state[variable_to_try], a):

                # Mark this attempt on the state for this variable.
                state[variable_to_try] = State.attempted(
                    state[variable_to_try], a)
                assignment[variable_to_try] = a

                # Record that we attempted a solution.
                tried_something = True

                # If we assign this literal value a, the negated version of this
                # literal will be false. Ensure that this assignment doesn't cause any
                # contradictions by updating watchlist.

                false_literal = Literal(instance.variables[variable_to_try], a)
                if instance.update_watchlist(false_literal, assignment):
                    # The proposed assignment is okay, keep it.
                    if verbose:
                        print("   attempted %i, succeed." % a)

                    # d += 1
                    found_sat = True
                    previous_attempts.append((to_attempt.pop(idx), idx))
                    break
                else:
                    # The proposed assignment causes a contradiction, revert it.
                    assignment[variable_to_try] = None
                    if verbose:
                        print("   attempted %i, failed." % a)

        # If we were unable to attempt a solution, backtrack if possible.
        if not tried_something:
            # if d == 0:
            if not previous_attempts:

                # Nowhere else to backtrack, no solutions.
                return "UNSAT"

            else:

                if verbose:
                    print("   Backtracking...")

                state[variable_to_try] = State(0)
                assignment[variable_to_try] = None
                prev = previous_attempts.pop()
                to_attempt.insert(prev[1], prev[0])

        # elif not found_sat and state[variable_to_try] == State.TRIED_BOTH:

        #     if verbose:
        #         print("   Backtracking, tried both...")

        #     state[variable_to_try] = State(0)
        #     assignment[variable_to_try] = None
        #     to_attempt.insert(idx, previous_attempts.pop())
