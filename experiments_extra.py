"""Doplnkove experimenty (pouzivaju run_once a show z experiments.py).

  A) vplyv limitu bocnych krokov          (N dam)
  B) vplyv poctu restartov                (TSP berlin52, 2-opt)
  C) skalovanie s velkostou problemu      (N dam)

Pouzitie:
    python experiments_extra.py --runs 10            # vsetky tri
    python experiments_extra.py --only A --runs 15   # len jeden
Vysledky idu na vystup a do results_extra.csv.
"""
import argparse
import statistics as st

from experiments import ALGOS, run_once, show
from nqueens import NQueens
from tsp import TSP, BERLIN52

OUT = "results_extra.csv"


def exp_sideways(runs, sizes=(10, 15), limits=(0, 3, 5, 10, 15)):
    """A) Kolko bocnych krokov staci? Bez restartov, aby bol vidiet cisty efekt."""
    hdr = ["N", "algorithm", "max_sideways", "success_%", "mean_steps", "mean_conflicts", "mean_evals"]
    for n in sizes:
        p, rows = NQueens(n), []
        for name, algo in ALGOS.items():
            for lim in limits:
                res = [run_once(algo, p, 2000 + k, lim, 0) for k in range(runs)]
                rows.append([n, name, lim,
                             f"{100 * sum(x.solved for x in res) / runs:.0f}",
                             f"{st.mean(x.steps for x in res):.1f}",
                             f"{st.mean(x.cost for x in res):.2f}",
                             f"{st.mean(x.evals for x in res):.0f}"])
        print(f"== A) bocne kroky, N={n}, {runs} behov")
        show(hdr, rows, OUT)


def exp_restarts(runs, counts=(1, 3, 5, 10, 15)):
    """B) Oplati sa viac restartov? TSP berlin52 s 2-opt, gap voci optimu 7542."""
    p = TSP(BERLIN52, "2opt", "berlin52", 7542)
    hdr = ["algorithm", "restarts", "mean_len", "std", "best", "gap_%", "mean_evals"]
    rows = []
    for name, algo in ALGOS.items():
        for r in counts:
            res = [run_once(algo, p, 3000 + k, 0, r if r > 1 else 0) for k in range(runs)]
            c = [x.cost for x in res]
            rows.append([name, r, f"{st.mean(c):.1f}", f"{st.pstdev(c):.1f}", f"{min(c):.1f}",
                         f"{100 * (st.mean(c) - 7542) / 7542:.2f}",
                         f"{st.mean(x.evals for x in res):.0f}"])
    print(f"== B) pocet restartov, berlin52 / 2-opt, {runs} behov")
    show(hdr, rows, OUT)


def exp_scaling(runs, sizes=(6, 8, 10, 12, 15), sideways=15):
    """C) Ako rastie narocnost s N? Bocne kroky zapnute, bez restartov."""
    hdr = ["N", "algorithm", "success_%", "mean_steps", "mean_evals"]
    rows = []
    for n in sizes:
        p = NQueens(n)
        for name, algo in ALGOS.items():
            res = [run_once(algo, p, 4000 + k, sideways, 0) for k in range(runs)]
            rows.append([n, name,
                         f"{100 * sum(x.solved for x in res) / runs:.0f}",
                         f"{st.mean(x.steps for x in res):.1f}",
                         f"{st.mean(x.evals for x in res):.0f}"])
    print(f"== C) skalovanie N dam (bocne kroky = {sideways}), {runs} behov")
    show(hdr, rows, OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--only", choices=["A", "B", "C"])
    a = ap.parse_args()
    open(OUT, "w").close()
    if a.only in (None, "A"):
        exp_sideways(a.runs)
    if a.only in (None, "B"):
        exp_restarts(a.runs)
    if a.only in (None, "C"):
        exp_scaling(a.runs)
