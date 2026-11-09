"""Best improvement (steepest ascent): v kazdom kroku prejde VSETKYCH susedov
a vyberie najlepsieho. Pri rovnosti vyberie nahodne.

max_sideways: kolko po sebe iducich bocnych krokov (delta == 0) smie spravit
              na plosine. 0 = ziadne (zakladna verzia).
"""
from base import Result, EPS


def best_improvement(problem, rng, max_sideways=0, max_steps=100000, state=None):
    if state is None:
        state = problem.random_state(rng)
    cost = problem.cost(state)
    moves = problem.moves()
    steps = evals = side = 0

    while steps < max_steps and not problem.is_goal(cost):
        best_delta = float("inf")
        candidates = []
        for m in moves:
            d = problem.delta(state, m)
            evals += 1
            if d < best_delta - EPS:
                best_delta, candidates = d, [m]
            elif abs(d - best_delta) <= EPS:
                candidates.append(m)

        if best_delta < -EPS:            # skutocne zlepsenie
            side = 0
        elif abs(best_delta) <= EPS and side < max_sideways:  # plosina
            side += 1
        else:                            # lokalne optimum
            break

        problem.apply(state, rng.choice(candidates))
        cost += best_delta
        steps += 1

    return Result(state, problem.cost(state), steps, evals, problem.is_goal(cost))
