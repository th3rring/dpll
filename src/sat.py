from instance import State
from instance import Literal
from utils import timerDecorator
from utils import Timer


def solve(instance, assignment, splitting, unit, verbose):

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

        # Update instance for the current assignment.
        instance.update_assignment(assignment)

        backtrack = True
        preformed_up = False

        # Run unit-preference.
        if instance.n_clauses[1]:

            unit_clauses = instance.n_clauses[1]

            # TODO:  <16-12-20, Therring> Make this a lambda function from input.
            unit_clause_index = unit(instance)
            variable_to_try = unit_clauses[unit_clause_index].unassigned[0]
            sat_assignment = unit_clauses[
                unit_clause_index].get_literal_from_var(
                    variable_to_try).negated ^ True

            # Find the to_attempt index of this variable.

            if verbose:
                print("Attempting UP %i" % variable_to_try)
                print("   to_attempt: {}".format(to_attempt))
                print("   previous_attempts: {}".format(previous_attempts))
                print("   state: {}".format(state))
                print("   assignment: {}".format(assignment))
            idx = to_attempt.index(variable_to_try)

            if State.can_try(state[variable_to_try], sat_assignment):

                # Mark this attempt on the state for this variable.
                # state[variable_to_try] = State.TRIED_BOTH
                state[variable_to_try] = State.attempted(
                    state[variable_to_try], sat_assignment)
                assignment[variable_to_try] = sat_assignment

                # Record that we attempted a solution.
                backtrack = False

                false_literal = Literal(instance.variables[variable_to_try],
                                        sat_assignment)
                if instance.update_watchlist(false_literal, assignment):
                    # The proposed assignment is okay, keep it.
                    if verbose:
                        print("   attempted %i, succeed." % sat_assignment)

                    previous_attempts.append((to_attempt.pop(idx), idx))
                else:

                    if verbose:
                        print("   attempted %i, failed." % sat_assignment)
                    # backtrack = True
                    assignment[variable_to_try] = None

            # if backtrack:
            #     if verbose:
            #         print("   Backtracking...")

            #     state[variable_to_try] = State(0)
            #     assignment[variable_to_try] = None

            #     # Trying to reset previous as well.
            #     prev = previous_attempts.pop()
            #     assignment[prev[0]] = None
            #     to_attempt.insert(prev[1], prev[0])

        else:

            # tried_something = False
            idx = None
            variable_to_try = None

            # Try the first element of to_attempt.
            idx = splitting(instance, to_attempt, assignment)
            variable_to_try = to_attempt[idx]

            if verbose:
                print("Attempting %i" % variable_to_try)
                print("   to_attempt: {}".format(to_attempt))
                print("   previous_attempts: {}".format(previous_attempts))
                print("   state: {}".format(state))
                print("   assignment: {}".format(assignment))

            for a in [False, True]:

                # Check if we can attempt this assignment.
                if State.can_try(state[variable_to_try], a):

                    # Mark this attempt on the state for this variable.
                    state[variable_to_try] = State.attempted(
                        state[variable_to_try], a)
                    assignment[variable_to_try] = a

                    # Record that we attempted a solution.
                    # tried_something = True
                    backtrack = False

                    # If we assign this literal value a, the negated version of this
                    # literal will be false. Ensure that this assignment doesn't cause any
                    # contradictions by updating watchlist.

                    false_literal = Literal(
                        instance.variables[variable_to_try], a)
                    if instance.update_watchlist(false_literal, assignment):
                        # The proposed assignment is okay, keep it.
                        if verbose:
                            print("   attempted %i, succeed." % a)

                        previous_attempts.append((to_attempt.pop(idx), idx))
                        break
                    else:
                        # The proposed assignment causes a contradiction, revert it.
                        assignment[variable_to_try] = None
                        if verbose:
                            print("   attempted %i, failed." % a)

            # If we were unable to attempt a solution, backtrack if possible.
            # if not tried_something:
            #     # if d == 0:
            #     if not previous_attempts:

            #         # Nowhere else to backtrack, no solutions.
            #         return "UNSAT"

            #     else:

            #         if verbose:
            #             print("   Backtracking...")

            #         state[variable_to_try] = State(0)
            #         assignment[variable_to_try] = None
            #         prev = previous_attempts.pop()
            #         to_attempt.insert(prev[1], prev[0])

        if backtrack:
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
                # assignment[prev[0]] = None
                to_attempt.insert(prev[1], prev[0])

        # elif not found_sat and state[variable_to_try] == State.TRIED_BOTH:

        #     if verbose:
        #         print("   Backtracking, tried both...")

        #     state[variable_to_try] = State(0)
        #     assignment[variable_to_try] = None
        #     to_attempt.insert(idx, previous_attempts.pop())
