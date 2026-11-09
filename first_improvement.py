"""First improvement: susedov prechadza v nahodnom poradi a prejde na
PRVEHO, ktory je lepsi. Lacnejsi krok ako best improvement.

Ak nenajde zlepsenie, ale videl suseda s delta == 0, moze spravit bocny krok
(najviac max_sideways po sebe).
"""
from base import Result, EPS


def first_improvement(problem, rng, max_sideways=0, max_steps=100000, state=None):
    if state is None:
        state = problem.random_state(rng)
    cost = problem.cost(state)
    moves = problem.moves()
    steps = evals = side = 0

    while steps < max_steps and not problem.is_goal(cost):
        order = list(moves)
        rng.shuffle(order)
        chosen, chosen_delta, zero_move = None, 0.0, None
        for m in order:
            d = problem.delta(state, m)
            evals += 1
            if d < -EPS:
                chosen, chosen_delta = m, d
                break
            if zero_move is None and abs(d) <= EPS:
                zero_move = m

        if chosen is not None:
            side = 0
        elif zero_move is not None and side < max_sideways:
            chosen, chosen_delta = zero_move, 0.0
            side += 1
        else:
            break

        problem.apply(state, chosen)
        cost += chosen_delta
        steps += 1

    return Result(state, problem.cost(state), steps, evals, problem.is_goal(cost))
