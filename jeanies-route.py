#!/bin/python3

import os
import sys

#
# Complete the jeanisRoute function below.
#
def jeanisRoute(k, roads):
    # city: globális lista, amely a levelek célvárosait tartalmazza
    global city

    # Csak az egyedi célvárosok számítanak
    required_cities = set(city)
    K_eff = len(required_cities)

    # Ha legfeljebb egy különböző városba kell menni, nem kell utazni
    if K_eff <= 1:
        return 0

    # Városok száma: fa, tehát N = (élek száma) + 1
    N = len(roads) + 1

    # Eredeti fa felépítése
    adj = [[] for _ in range(N + 1)]
    for u, v, d in roads:
        adj[u].append((v, d))
        adj[v].append((u, d))

    # Megjelöljük, mely csúcsok fontosak (ahova levél megy)
    required = [False] * (N + 1)
    for c in required_cities:
        required[c] = True

    # 1. lépés: fa gyökölése (tetszőleges gyök, pl. 1)
    root = 1
    parent = [-1] * (N + 1)
    parent_w = [0] * (N + 1)
    order = [root]
    parent[root] = 0  # 0 jelzi: nincs szülő

    # Iteratív bejárás: az 'order' lista olyan sorrendben veszi fel a csúcsokat,
    # hogy a szülő mindig előbb szerepel, mint a gyerek
    for u in order:
        for v, w in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            parent_w[v] = w
            order.append(v)

    # 2. lépés: cnt[u] = hány fontos csúcs van az u gyökerű részfában
    cnt = [0] * (N + 1)
    for u in reversed(order):
        if required[u]:
            cnt[u] += 1
        if u != root:
            cnt[parent[u]] += cnt[u]

    # 3. lépés: Steiner-fa (minimális részfa) felépítése és súlyösszeg
    total_weight = 0
    steiner_adj = [[] for _ in range(N + 1)]

    # Él (parent[v] - v) akkor kell a Steiner-fába, ha
    # 0 < cnt[v] < K_eff  (mindkét oldalán marad fontos csúcs)
    for v in range(1, N + 1):
        if v == root:
            continue
        if 0 < cnt[v] < K_eff:
            p = parent[v]
            w = parent_w[v]
            total_weight += w
            steiner_adj[v].append((p, w))
            steiner_adj[p].append((v, w))

    # Ha valamiért nincs él a Steiner-fában (K_eff > 1 mellett ez nem jellemző),
    # akkor nincs mit járni.
    start = None
    for i in range(1, N + 1):
        if steiner_adj[i]:
            start = i
            break
    if start is None:
        return 0

    # Segédfüggvény: legmesszebb levő csúcs keresése adott kezdőpontból
    def farthest(start_node):
        dist = [-1] * (N + 1)
        dist[start_node] = 0
        stack = [start_node]
        maxd = 0
        maxv = start_node
        while stack:
            u = stack.pop()
            for v, w in steiner_adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    if dist[v] > maxd:
                        maxd = dist[v]
                        maxv = v
                    stack.append(v)
        return maxv, maxd

    # 4. lépés: Steiner-fa átmérője két DFS-sel (iteratív)
    a, _ = farthest(start)
    b, diameter = farthest(a)

    # Minimális út: 2 * (Steiner-fa összsúlya) - átmérő
    answer = 2 * total_weight - diameter
    return answer


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()

    n = int(nk[0])
    k = int(nk[1])

    city = list(map(int, input().rstrip().split()))

    roads = []
    for _ in range(n - 1):
        roads.append(list(map(int, input().rstrip().split())))

    result = jeanisRoute(k, roads)

    fptr.write(str(result) + '\n')
    fptr.close()
