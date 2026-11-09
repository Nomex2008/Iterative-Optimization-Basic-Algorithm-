"""Problem obchodneho cestujuceho (TSP). Stav: permutacia miest (zoznam).
Cena = dlzka uzavretej trasy. Okolie podla `neighborhood`:
  "swap" - vymena dvoch miest (i, j)
  "2opt" - otocenie useku trasy t[i..j]
Delta sa pocita z 2 (2-opt) resp. 4 (swap) zmenenych hran, v O(1)."""
import math


class TSP:
    def __init__(self, coords, neighborhood="2opt", name="tsp", optimum=None):
        self.coords, self.n = coords, len(coords)
        self.neighborhood, self.name, self.optimum = neighborhood, name, optimum
        self.dist = [[math.hypot(a[0] - b[0], a[1] - b[1]) for b in coords] for a in coords]
        n = self.n
        # (0, n-1) vynechavame: v cykle je to degenerovany pripad
        self._moves = [(i, j) for i in range(n) for j in range(i + 1, n)
                       if not (i == 0 and j == n - 1)]

    @staticmethod
    def random_instance(n, rng, size=1000):
        return [(rng.uniform(0, size), rng.uniform(0, size)) for _ in range(n)]

    def random_state(self, rng):
        t = list(range(self.n))
        rng.shuffle(t)
        return t

    def cost(self, t):
        d = self.dist
        return sum(d[t[i - 1]][t[i]] for i in range(self.n))

    def moves(self):
        return self._moves

    def delta(self, t, move):
        i, j = move
        d, n = self.dist, self.n
        a, b, e, f = t[i - 1], t[i], t[j], t[(j + 1) % n]
        if self.neighborhood == "2opt":
            return d[a][e] + d[b][f] - d[a][b] - d[e][f]
        c, dd = t[(i + 1) % n], t[j - 1]
        if j == i + 1:
            return d[a][e] + d[b][f] - d[a][b] - d[e][f]
        return (d[a][e] + d[e][c] + d[dd][b] + d[b][f]
                - d[a][b] - d[b][c] - d[dd][e] - d[e][f])

    def apply(self, t, move):
        i, j = move
        if self.neighborhood == "2opt":
            t[i:j + 1] = t[i:j + 1][::-1]
        else:
            t[i], t[j] = t[j], t[i]

    def copy(self, t):
        return list(t)

    def is_goal(self, cost):
        return self.optimum is not None and cost <= self.optimum + 1e-6


# berlin52 z TSPLIB, znama optimalna dlzka = 7542 (euklidovska, zaokruhlena)
# POZOR: skontrolujte suradnice s TSPLIB suborom berlin52.tsp
BERLIN52 = [
    (565, 575), (25, 185), (345, 750), (945, 685), (845, 655), (880, 660),
    (25, 230), (525, 1000), (580, 1175), (650, 1130), (1605, 620), (1220, 580),
    (1465, 200), (1530, 5), (845, 680), (725, 370), (145, 665), (415, 635),
    (510, 875), (560, 365), (300, 465), (520, 585), (480, 415), (835, 625),
    (975, 580), (1215, 245), (1320, 315), (1250, 400), (660, 180), (410, 250),
    (420, 555), (575, 665), (1150, 1160), (700, 580), (685, 595), (685, 610),
    (770, 610), (795, 645), (720, 635), (760, 650), (475, 960), (95, 260),
    (875, 920), (700, 500), (555, 815), (830, 485), (1170, 65), (830, 610),
    (605, 625), (595, 360), (1340, 725), (1740, 245),
]
