"""Experimenty: kazda konfiguracia sa spusti `runs`-krat s rovnakymi seedmi
a vypisu sa priemery. Vysledky idu aj do CSV.

Pouzitie:  python experiments.py --runs 10
           python experiments.py --quick        (rychly test)
"""
import argparse, csv, random, statistics as st, time
from best_improvement import best_improvement
from first_improvement import first_improvement
from stochastic_hill_climbing import stochastic_hill_climbing
from random_restart import random_restart
from tsp import TSP, BERLIN52
from nqueens import NQueens

ALGOS = {"best": best_improvement, "first": first_improvement,
         "stochastic": stochastic_hill_climbing}
# (nazov, bocne kroky, pouzit restarty?)
VARIANTS = [("plain", 0, False), ("sideways", 15, False),
            ("restarts", 0, True), ("sideways+restarts", 15, True)]


def run_once(algo, problem, seed, sideways, restarts):
    rng = random.Random(seed)
    if restarts:
        return random_restart(algo, problem, rng, max_restarts=restarts, max_sideways=sideways)
    return algo(problem, rng, max_sideways=sideways)


def run_config(problem, runs, restarts, label_extra=""):
    rows = []
    for algo_name, algo in ALGOS.items():
        for var, side, use_r in VARIANTS:
            t0 = time.time()
            res = [run_once(algo, problem, 1000 + k, side, restarts if use_r else 0)
                   for k in range(runs)]
            rows.append(dict(problem=problem.name + label_extra, algorithm=algo_name,
                             variant=var, results=res, time=time.time() - t0))
    return rows


def summarize_tsp(rows, reference):
    out = []
    for r in rows:
        c = [x.cost for x in r["results"]]
        out.append([r["problem"], r["algorithm"], r["variant"],
                    f"{st.mean(c):.1f}", f"{st.pstdev(c):.1f}", f"{min(c):.1f}",
                    f"{100 * (st.mean(c) - reference) / reference:.2f}",
                    f"{st.mean(x.evals for x in r['results']):.0f}",
                    f"{r['time']:.1f}"])
    return out


def summarize_queens(rows):
    out = []
    for r in rows:
        res = r["results"]
        solved = [x for x in res if x.solved]
        out.append([r["problem"], r["algorithm"], r["variant"],
                    f"{100 * len(solved) / len(res):.0f}",
                    f"{st.mean(x.steps for x in res):.1f}",
                    f"{st.mean(x.cost for x in res):.2f}",
                    f"{st.mean(x.evals for x in res):.0f}",
                    f"{r['time']:.1f}"])
    return out


def show(header, table, path):
    widths = [max(len(str(x)) for x in col) for col in zip(header, *table)]
    line = lambda row: "  ".join(str(x).ljust(w) for x, w in zip(row, widths))
    print(line(header)); print("-" * (sum(widths) + 2 * len(widths)))
    for row in table:
        print(line(row))
    print()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(table); w.writerow([])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--tsp-sizes", type=int, nargs="*", default=[10, 15])
    ap.add_argument("--queens", type=int, nargs="*", default=[8, 12, 15])
    ap.add_argument("--no-berlin", action="store_true")
    ap.add_argument("--restarts", type=int, default=10)
    a = ap.parse_args()
    if a.quick:
        a.runs, a.tsp_sizes, a.queens, a.no_berlin = 5, [10], [8, 12], True

    open("results_tsp.csv", "w").close(); open("results_queens.csv", "w").close()

    # ---- TSP ----
    instances = [(f"rand{n}", TSP.random_instance(n, random.Random(n)), None) for n in a.tsp_sizes]
    if not a.no_berlin:
        instances.append(("berlin52", BERLIN52, 7542))
    hdr = ["instance", "algorithm", "variant", "mean_len", "std", "best", "gap_%", "mean_evals", "sec"]
    for hood in ("swap", "2opt"):
        all_rows = []
        for name, coords, opt in instances:
            all_rows.append((name, opt, run_config(TSP(coords, hood, f"{name}/{hood}", opt), a.runs, a.restarts)))
        for name, opt, rows in all_rows:
            ref = opt if opt else min(x.cost for r in rows for x in r["results"])
            note = "optimum" if opt else "najlepsie najdene"
            print(f"== TSP {name}, okolie {hood}, {a.runs} behov, gap voci: {note} ({ref:.1f})")
            show(hdr, summarize_tsp(rows, ref), "results_tsp.csv")

    # ---- N dam ----
    hdr = ["problem", "algorithm", "variant", "success_%", "mean_steps", "mean_conflicts", "mean_evals", "sec"]
    for n in a.queens:
        rows = run_config(NQueens(n), a.runs, a.restarts)
        print(f"== N dam, N={n}, {a.runs} behov")
        show(hdr, summarize_queens(rows), "results_queens.csv")


if __name__ == "__main__":
    main()
