from instance import State
from instance import Literal
from utils import timerDecorator
from utils import Timer


def solve(instance, assignment, splitting, unit_preference, verbose):

    # Init variables for state.
    n = len(instance.variables)
    state = [State(0)] * n

    # Init variables to what we've done.
    to_attempt = list(range(0, n))
    previous_attempts = []

    # Init boolean to hold backtracking state.
    backtrack = False

    # Variable to track number of calls.
    num_calls = 0

    # Main loop!
    while True:

        # Increment number of calls:
        num_calls += 1

        # If we reach here and there's nothing to attempt, we've solved it.
        if not to_attempt:
            # We return the first sat result we get.
            return assignment, num_calls

        # Init variables for this run.
        var_to_try = None
        idx = None
        unit_prop = False
        potentials = []

        if backtrack:

            # Get the previous assignment.
            prev = previous_attempts.pop()

            var_to_try = prev[0]
            idx = prev[1]
            unit_prop = prev[2]
            potentials = prev[3]

            # Reset assignment for the backtrack variable.
            assignment[prev[0]] = None

            # Add the backtracking variable back to attempt.
            to_attempt.insert(prev[1], prev[0])

            if verbose:
                print("Backtracking {} {}".format("UP" if unit_prop else "",
                                                  var_to_try))
                print("   unit_prop: {}".format(unit_prop))
                print("   potentials: {}".format(potentials))
                print("   to_attempt: {}".format(to_attempt))
                print("   previous_attempts: {}".format(previous_attempts))
                print("   state: {}".format(state))
                print("   assignment: {}".format(assignment))

        # Update instance for the current assignment.
        instance.update_assignment(assignment)

        # Choose a variable to try if we aren't backtracking.
        if not backtrack:

            # If we're not backtracking, decide to do unit pref or splitting.
            if instance.n_clauses[1]:

                # Get a list of all current unit clauses.
                unit_clauses = instance.n_clauses[1]

                # Choose a unit clause to attempt assignment using our lambda.
                unit_clause_index = unit_preference(instance)

                # Get the variable from the selected unit clause.
                var_to_try = unit_clauses[unit_clause_index].unassigned[0]

                # Find the to_attempt index of this variable.
                idx = to_attempt.index(var_to_try)

                # Add the only valid assignment for this unit proposition.
                potentials = [
                    unit_clauses[unit_clause_index].get_literal_from_var(
                        var_to_try).negated ^ True
                ]

                # set the unit clause to true.
                unit_prop = True

                if verbose:
                    print("Attempting UP %i" % var_to_try)
                    print("   to_attempt: {}".format(to_attempt))
                    print("   previous_attempts: {}".format(previous_attempts))
                    print("   state: {}".format(state))
                    print("   assignment: {}".format(assignment))

            else:

                # Choose an unassigned variable to try.
                idx = splitting(instance, to_attempt, assignment)
                var_to_try = to_attempt[idx]

                # Add both possible assignments.
                potentials = [False, True]

                # Mark that we're doing splitting.
                unit_prop = False

                if verbose:
                    print("Attempting %i" % var_to_try)
                    print("   to_attempt: {}".format(to_attempt))
                    print("   previous_attempts: {}".format(previous_attempts))
                    print("   state: {}".format(state))
                    print("   assignment: {}".format(assignment))

        # Set backtracking to True in case we cannot do any potential assignments.
        backtrack = True

        # Try possible assignments.
        for a in potentials:

            # Check if we can attempt this assignment.
            if State.can_try(state[var_to_try], a):

                # Mark this attempt on the state for this variable.
                state[var_to_try] = State.attempted(state[var_to_try], a)
                assignment[var_to_try] = a

                # If we assign this literal value a, the negated version of this
                # literal will be false. Ensure that this assignment doesn't cause any
                # contradictions by updating watchlist.
                false_literal = Literal(instance.variables[var_to_try], a)

                if instance.update_watchlist(false_literal, assignment):

                    # The proposed assignment is okay, keep it.
                    if verbose:
                        print("   attempted %i, succeed." % a)

                    # If we find any successful assignment, don't backtrack.
                    backtrack = False

                    # Record what we did here.
                    previous_attempts.append(
                        (to_attempt.pop(idx), idx, unit_prop, potentials))
                    break

                else:

                    # The proposed assignment causes a contradiction, revert it.
                    assignment[var_to_try] = None

                    if verbose:
                        print("   attempted %i, failed." % a)

        # If we have to backtrack, setup for next loop.
        if backtrack:
            if not previous_attempts:

                # Nowhere else to backtrack, no solutions.
                return "UNSAT", num_calls

            else:

                # Undo anything we did this loop and mark this variable as unassigned.
                state[var_to_try] = State(0)
                assignment[var_to_try] = None

                if verbose:
                    print("   Backtracking...")
