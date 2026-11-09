"""Spolocne veci pre vsetky algoritmy a problemy.

Rozhranie problemu (kazdy problem musi mat):
    random_state(rng)      -> nahodny pociatocny stav
    cost(state)            -> hodnota kriteria (minimalizujeme)
    moves()                -> zoznam vsetkych tahov okolia (nezavisi od stavu)
    delta(state, move)     -> zmena ceny, ak by sme tah spravili (stav sa NEMENI)
    apply(state, move)     -> vykona tah priamo na stave (in-place)
    copy(state)            -> kopia stavu
    is_goal(cost)          -> True, ak sme dosiahli ciel (da sa skoncit skor)
"""
from dataclasses import dataclass

EPS = 1e-9  # tolerancia pri porovnavani realnych cisel (TSP)


@dataclass
class Result:
    state: object      # najlepsi najdeny stav
    cost: float        # jeho cena
    steps: int         # pocet vykonanych tahov (krokov)
    evals: int         # pocet vyhodnoteni susedov (volani delta)
    solved: bool       # dosiahli sme ciel?
    restarts: int = 1  # kolko spusteni algoritmu sa pouzilo
