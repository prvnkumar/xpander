import matplotlib as mpl
mpl.use('Agg')
import json
import matplotlib.pyplot as plt
import random

from collections import defaultdict
from itertools import izip

import plot
from jellyfish import *
from routing import *
from xpander import *

LIFT_K = 2

def find_ksp_aatput(topo, ksp_k, fail_rates):
    """Average inter-switch tput when using ksp"""
    routing = Routing(topo)
    paths = routing.ksp(ksp_k)
    tput_vs_failure = dict()
    if 0.0 not in fail_rates:
        fail_rates.append(0.0)
    for fail_rate in fail_rates:
        tput = 0
        num_fail = int(len(topo.edges()) * fail_rate)
        failed_links = random.sample(set(topo.edges()), num_fail)
        for s in topo.nodes_iter():
            for d in topo.nodes_iter():
                if s != d:
                    num_paths = len(paths[s][d])
                    for path in paths[s][d]:
                        path_edges = set(izip(path, path[1:]))
                        if len(path_edges.intersection(failed_links)) == 0:
                            tput += 1.0/num_paths
        tput_vs_failure[fail_rate] = tput

    # normalize
    base_tput = tput_vs_failure[0.0]
    for k, v in tput_vs_failure.iteritems():
        tput_vs_failure[k] = v/base_tput
    return tput_vs_failure

def ksp_tput_fail_experiment(switch_k, num_servers_per_rack, ksp_k):
    # topo_type -> #failure -> tput
    ksptput = defaultdict(defaultdict)

    switch_d = switch_k - num_servers_per_rack
    num_servers = 176*3
    num_switches = int(math.ceil(num_servers/num_servers_per_rack))
    print num_switches
    if num_switches <= switch_d:
        return

    # We might not get the exact number of servers specified
    num_lifts = int(math.ceil(math.log(num_switches/(switch_d+1), LIFT_K)))
    num_servers = int(num_servers_per_rack * (switch_d + 1) * math.pow(LIFT_K, num_lifts))
    num_switches = num_servers/num_servers_per_rack
    print num_switches
    print "num_servers: ", num_servers

    x_topo = Xpander(num_servers, num_servers_per_rack, switch_d=switch_d,
                     lift_k=LIFT_K).G
    j_topo = Jellyfish(num_servers, num_servers_per_rack, switch_d).G
    fail_rates = [0.03 * f for f in range(11)]
    ksptput["xpander"] = find_ksp_aatput(x_topo, ksp_k, fail_rates)
    ksptput["jellyfish"] = find_ksp_aatput(j_topo, ksp_k, fail_rates)

    return ksptput

if __name__=="__main__":
    read_from_file = False
    for params in [(13, 3)]:
        file_name = "output/kspfail_" + str(params).replace(' ', '_')
        ksptput = defaultdict(defaultdict)
        if read_from_file:
            try:
                tmp_len = None
                with open(file_name + '.json', 'r') as f:
                    tmp_len = json.load(f)
                for topo, data in tmp_len.iteritems():
                    for k,v in data.iteritems():
                        ksptput[topo][float(k)] = float(v)
            except IOError:
                print "File not found."
        else:
            switch_k, num_servers_per_rack = params
            ksptput = ksp_tput_fail_experiment(switch_k,
                                          num_servers_per_rack,
                                          8)
            with open(file_name + '.json', 'w') as f:
                json.dump(ksptput, f)
        plot.plot_ksp_fail_tput(ksptput, file_name + ".pdf")
