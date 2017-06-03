import math
import matplotlib.pyplot as plt
import networkx as nx
import random

from mininet.topo import Topo

# Based on interpretation of https://people.inf.ethz.ch/asingla/papers/jellyfish-nsdi12.pdf 's Section 3

class Jellyfish(Topo):
    "Jellyfish topology."
    def __init__(self, num_servers, servers_per_rack, switch_d, draw=False, draw_output="", convert_to_topo=True):

        # Initialize topology
        Topo.__init__(self)
        num_switches = num_servers / servers_per_rack

        # Initialize with complete d-regular graph
        self.G = nx.random_regular_graph(switch_d, num_switches)

        if draw:
            self.draw_graph(self.G, draw_output)

        # Convert graph to mininet topology
        if convert_to_topo:
            self.graph_to_topo(self.G)

    def draw_graph(self, G, draw_output):
        pos=nx.circular_layout(G)
        nx.draw(G, pos)
        labels = dict(zip(G.nodes(), [str(x) for x in G.nodes_iter()]))
        nx.draw_networkx_labels(G, pos, labels)
        plt.draw()
        plt.savefig(draw_output)
        plt.clf()

    def graph_to_topo(self, G):
        for n in G.nodes_iter():
            self.addNode("s" + str(n))
        for e in G.edges_iter():
            self.addLink("s" + str(e[0]),
                         "s" + str(e[1]))

    def add_one_node(self, draw=False, draw_output="incr_graph.png"):
        # Remove a random edge
        new_n = len(self.G.nodes()) + 1
        self.G.add_node(new_n)
        for (u, v) in random.sample(self.G.edges(), k=1):
            self.G.remove_edge(u, v)
            self.G.add_edge(new_n, u)
            self.G.add_edge(new_n, v)

        if draw:
            self.draw_graph(self.G, draw_output)

topos = { 'jellyfish': ( lambda: Jellyfish() ) }
