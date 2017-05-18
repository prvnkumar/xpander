import math
import matplotlib.pyplot as plt
import networkx as nx
import random

from mininet.topo import Topo

# Based on interpretation of https://people.inf.ethz.ch/asingla/papers/jellyfish-nsdi12.pdf 's Section 3

class Jellyfish(Topo):
    "Xpander topology."
    def __init__(self, num_servers, servers_per_rack, draw=True):

        # Initialize topology
        Topo.__init__(self)
	num_switches = num_servers / servers_per_rack

        # Initialize with complete d-regular graph
        self.G = self.create_regular(servers_per_rack, num_switches)

        if draw:
            self.draw_graph(self.G)

        # Convert graph to mininet topology
        self.graph_to_topo(self.G)

    def draw_graph(self, G):
        pos=nx.circular_layout(G)
        nx.draw(G, pos)
        labels = dict(zip(G.nodes(), [str(x) for x in G.nodes_iter()]))
        nx.draw_networkx_labels(G, pos, labels)
        plt.draw()
        plt.savefig("graph.png")

    def create_regular(self, d, N):
        return nx.random_regular_graph(d, N)

    def graph_to_topo(self, G):
        for n in G.nodes_iter():
            self.addNode("s" + str(n))
        for e in G.edges_iter():
            self.addLink("s" + str(e[0]),
                         "s" + str(e[1]))

topos = { 'jellyfish': ( lambda: Jellyfish() ) }
