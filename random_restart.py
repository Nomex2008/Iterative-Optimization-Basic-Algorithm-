"""Nahodne restarty: opakovane spusta zvoleny algoritmus z novych nahodnych
stavov, pamata si najlepsi vysledok a konci, ked najde ciel alebo vycerpa restarty.
"""
from base import Result


def random_restart(algorithm, problem, rng, max_restarts=10, **kwargs):
    best = None
    steps = evals = used = 0
    for _ in range(max_restarts):
        res = algorithm(problem, rng, **kwargs)
        used += 1
        steps += res.steps
        evals += res.evals
        if best is None or res.cost < best.cost:
            best = res
        if res.solved:
            break
    return Result(best.state, best.cost, steps, evals, best.solved, used)
