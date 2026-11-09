"""Problem N dam. Stav: q[i] = riadok damy v stlpci i. Cena = pocet dvojic dam,
ktore sa ohrozuju (ciel 0). Pocitadla riadkov a diagonal => delta v O(1).
Tah = (stlpec, novy_riadok)."""
from base import Result


class QueensState:
    __slots__ = ("n", "q", "row", "d1", "d2", "cost")

    def __init__(self, q):
        n = len(q)
        self.n, self.q = n, list(q)
        self.row = [0] * n
        self.d1 = [0] * (2 * n - 1)   # diagonala c + r
        self.d2 = [0] * (2 * n - 1)   # diagonala c - r + n - 1
        for c, r in enumerate(q):
            self.row[r] += 1
            self.d1[c + r] += 1
            self.d2[c - r + n - 1] += 1
        self.cost = sum(k * (k - 1) // 2 for arr in (self.row, self.d1, self.d2) for k in arr)


class NQueens:
    def __init__(self, n):
        self.n = n
        self.name = f"{n}-queens"
        self._moves = [(c, r) for c in range(n) for r in range(n)]

    def random_state(self, rng):
        return QueensState([rng.randrange(self.n) for _ in range(self.n)])

    def cost(self, s):
        return s.cost

    def moves(self):
        return self._moves

    def delta(self, s, move):
        c, r = move
        ro = s.q[c]
        if r == ro:
            return float("inf")       # "tah" na mieste, nie je to sused
        n = s.n
        removed = (s.row[ro] - 1) + (s.d1[c + ro] - 1) + (s.d2[c - ro + n - 1] - 1)
        added = s.row[r] + s.d1[c + r] + s.d2[c - r + n - 1]
        return added - removed

    def apply(self, s, move):
        c, r = move
        d = self.delta(s, move)
        ro, n = s.q[c], s.n
        s.row[ro] -= 1; s.d1[c + ro] -= 1; s.d2[c - ro + n - 1] -= 1
        s.row[r] += 1;  s.d1[c + r] += 1;  s.d2[c - r + n - 1] += 1
        s.q[c] = r
        s.cost += d

    def copy(self, s):
        return QueensState(s.q)

    def is_goal(self, cost):
        return cost == 0
