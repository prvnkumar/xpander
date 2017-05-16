import matplotlib.pyplot as plt
import networkx as nx
import random

from mininet.topo import Topo

class Xpander(Topo):
    "Xpander topology."
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        self.d = 3
        G = self.create_regular(self.d)
        G = self.two_lift(G)
        G = self.two_lift(G)
        self.draw_graph(G)
        self.graph_to_topo(G)

    def draw_graph(self, G):
        pos=nx.circular_layout(G)
        nx.draw(G, pos)
        labels = dict(zip(G.nodes(), [str(x) for x in G.nodes_iter()]))
        nx.draw_networkx_labels(G, pos, labels)
        plt.draw()
        plt.savefig("g.png")

    def create_regular(self, d):
        return nx.random_regular_graph(d, d+1)

    def two_lift(self, G):
        mapping = dict(zip(G.nodes(), [2*x for x in G.nodes()] ))
        G = nx.relabel_nodes(G,mapping)
        original_nodes = G.nodes()
        new_nodes = [n+1 for n in original_nodes]
        for n in new_nodes:
            G.add_node(n)
        for s,d in G.edges():
            print s,d
            G.remove_edge(s,d)
            if bool(random.getrandbits(1)):
                G.add_edge(s,d)
                G.add_edge(s+1,d+1)
            else:
                G.add_edge(s+1,d)
                G.add_edge(s,d+1)
        return G

    def graph_to_topo(self, G):
        for n in G.nodes_iter():
            self.addNode("s" + str(n))
        for e in G.edges_iter():
            self.addLink("s" + str(e[0]),
                         "s" + str(e[1]))

topos = { 'xpander': ( lambda: Xpander() ) }
