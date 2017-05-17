import networkx as nx

from collections import defaultdict
from itertools import islice

class Routing():
    " Class to implement routing algorithms."
    def __init__(self, G):
        self.G = G

    def ksp(self, k):
        paths = defaultdict(defaultdict)
        for src in self.G.nodes_iter():
            for dst in self.G.nodes_iter():
                if src != dst:
                    paths[src][dst] = self.k_shortest_paths(src, dst, k)
        return paths

    def k_shortest_paths(self, source, target, k=4, weight=None):
        return list(islice(nx.shortest_simple_paths(
            self.G, source, target, weight=weight), k))
