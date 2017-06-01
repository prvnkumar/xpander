import matplotlib as mpl
mpl.use('Agg')
import json
import matplotlib.pyplot as plt
import pulp

from collections import defaultdict
from itertools import izip

import plot
from jellyfish import *
from routing import *
from xpander import *
from avg_shortest_path import *

LIFT_K = 2

def aatput_ub(N, r, f):
    opt_d = avgsp_lb(N, r)
    maxtput = (N * r) / (f * opt_d)
    return maxtput

def find_max_aatput(g):
    """Solve MCF as LP for uniform all-to-all demand and return max possible
    tput"""
    # convert into a directed graph
    topo = g.to_directed()
    edges = sorted(topo.edges())
    nodes = sorted(topo.nodes())
    # all-to-all demands
    demands = []
    for s in nodes:
        for d in nodes:
            if s != d:
                demands.append((s,d))
    prob = pulp.LpProblem("MCF", pulp.LpMinimize)

    # Create flow variables for each edge
    edge_flows = {}
    for e in edges:
        for d in demands:
            name = "L{}_{}_D{}_{}".format(e[0], e[1], d[0], d[1])
            edge_flows[(e, d)] = pulp.LpVariable(name, 0)

    # objective function = var Z
    objective = pulp.LpVariable('Z', 0)
    prob += objective

    # capacity constraints
    for e in edges:
        tmp_list = [-1 * objective]
        for d in demands:
            tmp_list.append(edge_flows[(e, d)])
        edgename = "E{}_{}".format(e[0], e[1])
        prob += pulp.lpSum(tmp_list)<= 0, "Cap|" + edgename
    # flow conservation constraints
    for v in nodes:
        for d in demands:
            tmp_list = []
            in_edges = topo.in_edges(v)
            out_edges = topo.out_edges(v)
            for e in out_edges:
                tmp_list.append(edge_flows[(e, d)])
            for e in in_edges:
                tmp_list.append(-1.0 * edge_flows[(e, d)])
            rhs = 0.0
            if v == d[0]:
                rhs = 1
            if v == d[1]:
                rhs = -1
            constraint_name = "Cons|{}D{}_{}".format(v, d[0], d[1])
            prob += pulp.lpSum(tmp_list) == rhs, constraint_name
    prob.solve()
    maxutil = pulp.value(prob.objective)
    print "MCF maxutil", maxutil
    return 1./maxutil


def all_to_all_tput_experiment(switch_k, num_servers_per_rack):
    aatput = defaultdict(defaultdict) # topo_type -> num_servers -> tput
    switch_d = switch_k - num_servers_per_rack
    for num_servers in [(1 << i) for i in range(5, 12)]:
        # Might not get the exact number of servers as specified
        num_servers = xpander_num_servers(num_servers, num_servers_per_rack,
                                          switch_d, LIFT_K)
        if num_servers is None:
            continue
        num_switches = num_servers / num_servers_per_rack
        print "num_servers: ", num_servers

        x_topo = Xpander(num_servers, num_servers_per_rack, switch_d=switch_d,
                         lift_k=LIFT_K).G
        j_topo = Jellyfish(num_servers, num_servers_per_rack, switch_d).G

        aatput["xpander"][num_servers] = find_max_aatput(x_topo)
        aatput["jellyfish"][num_servers] = find_max_aatput(j_topo)

        # Normalize by theoretical limit
        opt_aatput = aatput_ub(num_switches,
                               switch_d,
                               num_switches * (num_switches - 1))
        aatput["xpander"][num_servers] /= opt_aatput
        aatput["jellyfish"][num_servers] /= opt_aatput
    return aatput

if __name__=="__main__":
    read_from_file = False
    for params in [(14,4), (18,4)]:
        file_name = "output/aa_" + str(params).replace(' ', '_')
        aatput = defaultdict(defaultdict)
        if read_from_file:
            try:
                tmp_len = None
                with open(file_name + '.json', 'r') as f:
                    tmp_len = json.load(f)
                for topo, data in tmp_len.iteritems():
                    for k,v in data.iteritems():
                        aatput[topo][int(k)] = float(v)
            except IOError:
                print "File not found."
        else:
            switch_k, num_servers_per_rack = params
            aatput = all_to_all_tput_experiment(switch_k,
                                                num_servers_per_rack)
            with open(file_name + '.json', 'w') as f:
                json.dump(aatput, f)
        plot.plot_all_all_tput(aatput, file_name + ".pdf")
