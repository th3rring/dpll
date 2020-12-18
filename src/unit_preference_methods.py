from random import randrange


def random_choice(instance):
    return randrange(0, len(instance.n_clauses[1]))
