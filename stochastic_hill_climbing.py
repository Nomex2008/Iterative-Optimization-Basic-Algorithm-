"""Stochasticke iterativne vylepsovanie: nahodne vyberie JEDNEHO suseda
a prijme ho, ak je lepsi. Skonci, ked `patience` pokusov po sebe nepriniesla
zlepsenie (default = velkost okolia, takze je to priblizne "ziadny lepsi sused").
"""
from base import Result, EPS


def stochastic_hill_climbing(problem, rng, max_sideways=0, max_steps=100000,
                             patience=None, state=None):
    if state is None:
        state = problem.random_state(rng)
    cost = problem.cost(state)
    moves = problem.moves()
    patience = patience or len(moves)
    steps = evals = side = fails = 0

    while steps < max_steps and fails < patience and not problem.is_goal(cost):
        m = rng.choice(moves)
        d = problem.delta(state, m)
        evals += 1
        if d < -EPS:
            problem.apply(state, m)
            cost += d
            steps += 1
            side = fails = 0
        elif abs(d) <= EPS and side < max_sideways:
            problem.apply(state, m)       # bocny krok
            steps += 1
            side += 1
            fails += 1
        else:
            fails += 1

    return Result(state, problem.cost(state), steps, evals, problem.is_goal(cost))
