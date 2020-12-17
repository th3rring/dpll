from enum import Enum
from collections import deque
from collections import defaultdict


class State(Enum):
    TRIED_NONE = 0
    TRIED_FALSE = 1
    TRIED_TRUE = 2
    TRIED_BOTH = 3

    def attempted(state, to_try):
        if state == State.TRIED_NONE:
            if to_try:
                return State.TRIED_TRUE
            else:
                return State.TRIED_FALSE
        elif ((state == State.TRIED_TRUE) and not to_try) or \
        ((state == State.TRIED_FALSE) and to_try):
            return State.TRIED_BOTH

    def can_try(state, to_try):
        return (state == State.TRIED_NONE) or \
         (state == State.TRIED_FALSE and to_try) or \
          (state == State.TRIED_TRUE and not to_try)

    def __repr__(self):
        return self.name


class Variable():
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return "Variable: %s (index: %i)" % (self.name, self.index)

    def __str__(self):
        return "Variable: %s (index: %i)" % (self.name, self.index)


class Literal():
    def __init__(self, var, negated):
        self.variable = var
        self.negated = negated

        # For loopup in watchlists, we use -index or index depending on
        # if the variable is negated. Save that here.
        self.encoding = ("-" if negated else "") + str(self.variable.index)

    def eval(self, val):
        return val ^ self.negated if val is not None else False

    def __repr__(self):
        return "Literal: %s (index: %i)" % (
            ("-" if self.negated else "") + self.variable.name,
            self.variable.index)

    def __str__(self):
        return "Literal: %s (index: %i)" % (
            ("-" if self.negated else "") + self.variable.name,
            self.variable.index)


class Clause():
    def __init__(self, literals):
        self.literals = literals
        self.variable_indexes = [l.variable.index for l in self.literals]
        self.unassigned = self.variable_indexes

    def __getitem__(self, index):
        return self.literals[0]

    def __iter__(self):
        return iter(self.literals)

    def __contains__(self, item):
        return item in self.get_variable_indexes()

    def __repr__(self):
        return "Clause: {}".format(self.literals)

    def __str__(self):
        return "Clause: {}".format(self.literals)

    def get_literal_from_var(self, var_index):
        for literal in self.literals:
            if literal.variable.index == var_index:
                return literal

    def get_variable_indexes(self):
        return self.variable_indexes

    def apply_assignment(self, assignment):
        unassigned = []
        for var in self.variable_indexes:
            if assignment[var] is None:
                unassigned.append(var)
        self.unassigned = unassigned

    def count_unassigned(self, assignment):
        self.apply_assignment(assignment)
        return len(self.unassigned)


class Instance():
    def __init__(self):
        self.variables = []
        self.variables_lookup = dict()
        self.clauses = []
        self.watchlist = defaultdict(deque)
        self.n_clauses = defaultdict(list)

    def update_assignment(self, assignment):
        n_clauses = defaultdict(list)

        for clause in self.clauses:

            # Ensure that we only update for unsat clauses.
            clause_sat = False
            for literal in clause:
                if literal.eval(assignment[literal.variable.index]):
                    clause_sat = True
                    break

            if not clause_sat:
                count = clause.count_unassigned(assignment)
                n_clauses[count].append(clause)

        self.n_clauses = n_clauses

    def parse_problem(self, string_problem):
        for line in string_problem.splitlines():
            self.add_clause(line)

    def add_clause(self, string_clause):

        cur_clause_list = []

        # Parse the string clause one literal at a time.
        for literal in string_clause.split():

            # Figure out if this literal is negated.
            negated = literal.startswith('-')

            # Capture the variable name.
            variable_name = literal
            if negated:
                variable_name = literal[1:]

            # Get the index of this new variable
            cur_index = len(self.variables)
            var_exists = False

            # If we've already seen this variable, pull up the existing index.
            if variable_name in self.variables_lookup:
                cur_index = self.variables_lookup[variable_name]
                var_exists = True

            var = Variable(variable_name, cur_index)

            # If we haven't seen this variable, add it to this instance.
            if not var_exists:
                self.variables.append(var)
                self.variables_lookup[variable_name] = cur_index

            # Create an instance of this variable and add to this clause.
            literal = Literal(var, negated)
            cur_clause_list.append(literal)

        # Add the completed clause to the clause list.
        cur_clause = Clause(cur_clause_list)
        self.clauses.append(cur_clause)

    def check_assignment(self, assignment):

        # Iterate through each clause.
        clause_sat = False
        for clause in self.clauses:

            # Ensure that at least one literal is true.
            # clause_sat = False
            for literal in clause:
                if literal.eval(assignment[literal.variable.index]):
                    clause_sat = True
                    break

        # If we can't find one, this isn't a sat assignment.
        if not clause_sat:
            return False
        return True

    def setup_watchlist(self):
        for clause in self.clauses:

            # Add the first literal in each clause.
            self.watchlist[clause[0].encoding].append(clause)

    def update_watchlist(self, false_literal, assignment):

        # Repeat updating the watchlist until we don't watch this variable anymore.
        while self.watchlist[false_literal.encoding]:

            alternate_exists = False

            # Look at the first clause being watched by the false literal.
            cur_clause = self.watchlist[false_literal.encoding][0]

            for alt_literal in cur_clause:

                # Calculate the required value of alt_literal to be satisfied.
                sat_value = alt_literal.negated ^ True

                if assignment[alt_literal.variable.index] is None or \
                  assignment[alt_literal.variable.index] == sat_value:

                    # We've found a satisfiable alternate literal.
                    alternate_exists = True

                    # Update the watchlist to show this and break out.
                    del self.watchlist[false_literal.encoding][0]
                    self.watchlist[alt_literal.encoding].append(cur_clause)
                    break

            if not alternate_exists:
                return False

        return True
