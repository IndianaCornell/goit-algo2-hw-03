from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0]*vertices for _ in range(vertices)]

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, source, sink, parent):
        visited = [False]*self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v, cap in enumerate(self.graph[u]):
                if not visited[v] and cap > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def edmonds_karp(self, source, sink):
        parent = [-1]*self.V
        max_flow = 0
        flows = [[0]*self.V for _ in range(self.V)]

        while self.bfs(source, sink, parent):
            path_flow = float("inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                flows[u][v] += path_flow
                v = parent[v]
        return max_flow, flows


if __name__ == "__main__":
    SRC, T1, T2 = 0, 1, 2
    WH1, WH2, WH3, WH4 = 3, 4, 5, 6
    STORES = list(range(7, 21))  
    SNK = 21

    g = Graph(22)

    g.add_edge(SRC, T1, 1000)
    g.add_edge(SRC, T2, 1000)

    g.add_edge(T1, WH1, 25)
    g.add_edge(T1, WH2, 20)
    g.add_edge(T1, WH3, 15)
    g.add_edge(T2, WH3, 15)
    g.add_edge(T2, WH4, 30)
    g.add_edge(T2, WH2, 10)

    def s(n): return 6 + n   

    g.add_edge(WH1, s(1), 15)
    g.add_edge(WH1, s(2), 10)
    g.add_edge(WH1, s(3), 20)
    g.add_edge(WH2, s(4), 15)
    g.add_edge(WH2, s(5), 10)
    g.add_edge(WH2, s(6), 25)
    g.add_edge(WH3, s(7), 20)
    g.add_edge(WH3, s(8), 15)
    g.add_edge(WH3, s(9), 10)
    g.add_edge(WH4, s(10), 20)
    g.add_edge(WH4, s(11), 10)
    g.add_edge(WH4, s(12), 15)
    g.add_edge(WH4, s(13), 5)
    g.add_edge(WH4, s(14), 10)

    for store in STORES:
        g.add_edge(store, SNK, 1000)

    max_flow, flows = g.edmonds_karp(SRC, SNK)
    print(f"Maximum flow: {max_flow}\n")
    print("Terminal\tStore\tActual Flow")

    for wh in [WH1, WH2, WH3, WH4]:
        inflow = {t: flows[t][wh] for t in [T1, T2] if flows[t][wh] > 0}
        total_in = sum(inflow.values())
        if total_in == 0:
            continue
        for store in range(7, 21):
            if flows[wh][store] > 0:
                for t, fin in inflow.items():
                    ratio = fin / total_in
                    terminal = "Terminal 1" if t == T1 else "Terminal 2"
                    store_name = f"Store {store - 6}"
                    amount = round(flows[wh][store] * ratio, 2)
                    print(f"{terminal}\t{store_name}\t{amount}")
