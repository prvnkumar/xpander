import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import random

from mininet.topo import Topo

debug = False

def log(msg):
    if debug:
        print msg

def xpander_num_servers(num_servers, num_servers_per_rack, switch_d, lift_k):
    num_switches = int(math.ceil(num_servers/num_servers_per_rack))
    if num_switches <= switch_d:
        return None
    num_lifts = int(math.ceil(math.log(num_switches/(switch_d+1), lift_k)))
    num_switches = int((switch_d + 1) * math.pow(lift_k, num_lifts))
    num_servers = num_switches * num_servers_per_rack
    return num_servers

class Xpander(Topo):
    "Xpander topology."
    def __init__(self, num_servers, servers_per_rack,
                 switch_d=3, lift_k=2, draw=False, draw_output="graph.png",
                 convert_to_topo=True):
        # Initialize topology
        Topo.__init__(self)
        self.switch_d = switch_d

        # Initialize with complete d-regular graph
        self.G = self.create_regular(self.switch_d)

        # Perform k-lifting
        num_switches = int(math.ceil(num_servers/servers_per_rack))
        log("Num Switches: " + str(num_switches))
        num_lifts = int(math.ceil(math.log(num_switches/(switch_d+1),
                                           lift_k)))
        log("Num Lifts: " + str(num_lifts))
        log("Actual number of hosts: " + str((servers_per_rack *
                                           (switch_d + 1) *
                                           math.pow(lift_k, num_lifts))))
        for lift_i in range(num_lifts):
            self.G = self.k_lift(self.G, lift_k)

        if draw:
            self.draw_graph(self.G, draw_output)

        # Convert graph to mininet topology
        if convert_to_topo:
            self.graph_to_topo(self.G)
    
    def add_one_node(self, draw=False, draw_output="incr_graph.png"):
        # Remove d/2 random edges 
        remove_k = int(math.ceil(self.switch_d/2))
        new_n = len(self.G.nodes()) + 1
        self.G.add_node(new_n)
        for (u, v) in random.sample(self.G.edges(), k=remove_k):
            self.G.remove_edge(u, v)
            self.G.add_edge(new_n, u)
            self.G.add_edge(new_n, v)
        
        if draw:
            self.draw_graph(self.G, draw_output)

    def draw_graph(self, G, draw_output):
        pos=nx.circular_layout(G)
        nx.draw(G, pos)
        labels = dict(zip(G.nodes(), [str(x) for x in G.nodes_iter()]))
        nx.draw_networkx_labels(G, pos, labels)
        plt.draw()
        plt.savefig(draw_output)
        plt.clf()

    def create_regular(self, d):
        return nx.random_regular_graph(d, d+1)

    def two_lift(self, G):
        mapping = dict(zip(G.nodes(), [2*x for x in G.nodes()] ))
        G = nx.relabel_nodes(G, mapping)
        original_nodes = G.nodes()
        new_nodes = [n+1 for n in original_nodes]
        for n in new_nodes:
            G.add_node(n)
        for u, v in G.edges():
            G.remove_edge(u, v)
            if bool(random.getrandbits(1)):
                G.add_edge(u,v)
                G.add_edge(u+1, v+1)
            else:
                G.add_edge(u+1, v)
                G.add_edge(u, v+1)
        return G

    def k_lift(self, G, k):
        mapping = dict(zip(G.nodes(), [k*x for x in G.nodes()]))
        G = nx.relabel_nodes(G, mapping)
        original_nodes = G.nodes()
        for n in original_nodes:
            for i in range(1, k):
                G.add_node(n+i)
        for u, v in G.edges():
            G.remove_edge(u, v)
            matching = list(range(k))
            random.shuffle(matching)
            for i in range(k):
                j = matching[i]
                G.add_edge(u+i, v+j)
        return G

    def graph_to_topo(self, G):
        for n in G.nodes_iter():
            self.addNode("s" + str(n))
        for e in G.edges_iter():
            self.addLink("s" + str(e[0]),
                         "s" + str(e[1]))

topos = { 'xpander': ( lambda: Xpander() ) }
