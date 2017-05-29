import matplotlib as mpl
mpl.use('Agg')
import json
import matplotlib.pyplot as plt
import pulp

from collections import defaultdict
from itertools import izip

from jellyfish import *
from routing import *
from xpander import *

LIFT_K = 2

def find_ksp_aatput(topo, ksp_k):
    """Average inter-switch tput when using ksp"""
    routing = Routing(topo)
    paths = routing.ksp(ksp_k)
    utilization = dict()
    max_util = 0.0
    for s in topo.nodes_iter():
        for d in topo.nodes_iter():
            if s != d:
                num_paths = len(paths[s][d])
                for path in paths[s][d]:
                    for edge in izip(path, path[1:]):
                        utilization[edge] = utilization.get(edge, 0) + 1.0/num_paths
                        max_util = max(max_util, utilization[edge])
    maxtput = 1./max_util
    return maxtput

def ksp_tput_experiment(switch_k, num_servers_per_rack, ksp_ks):
    # topo_type -> ksp_k -> num_servers -> tput
    ksptput = defaultdict(defaultdict)
    for ksp_k in ksp_ks:
            ksptput["xpander"][ksp_k] = dict()
            ksptput["jellyfish"][ksp_k] = dict()

    switch_d = switch_k - num_servers_per_rack
    for num_servers in [(1 << i) for i in range(6, 10)]:
        num_switches = int(math.ceil(num_servers/num_servers_per_rack))
        if num_switches <= switch_d:
            continue

        # We might not get the exact number of servers specified
        num_lifts = int(math.ceil(math.log(num_switches/(switch_d+1), LIFT_K)))
        num_servers = int(num_servers_per_rack * (switch_d + 1) * math.pow(LIFT_K, num_lifts))
        num_switches = num_servers/num_servers_per_rack
        print "num_servers: ", num_servers

        x_topo = Xpander(num_servers, num_servers_per_rack, switch_d=switch_d, lift_k=LIFT_K).G
        j_topo = Jellyfish(num_servers, num_servers_per_rack, switch_d).G
        for ksp_k in ksp_ks:
            ksptput["xpander"][ksp_k][num_servers] = find_ksp_aatput(x_topo,
                                                                     ksp_k)
            ksptput["jellyfish"][ksp_k][num_servers] = find_ksp_aatput(j_topo,
                                                                       ksp_k)

    return ksptput

getcolor = {"xpander" : "gray", "jellyfish" : "orange"}
getmarker = {"xpander" : "o", "jellyfish" : "s"}

def plot_all_all_tput(path_lengths, file_name):
    plt.figure(figsize=(6,4))
    for topo_type, k_data in path_lengths.iteritems():
        for ksp_k, data in k_data.iteritems():
            num_servers = sorted([int(k) for k in data.keys()])
            path_lengths = [float(data[i]) for i in num_servers]
            print data
            plt.plot(num_servers, path_lengths,
                     color = getcolor[topo_type],
                     linestyle = '-',
                     linewidth=4,
                     markersize=8,
                     marker = getmarker[topo_type],
                     label=topo_type + '-' + str(ksp_k))
    plt.xlabel("Number of servers")
    plt.ylabel("Avg. shortest paths")
    plt.legend(loc="best")
    plt.savefig(file_name)
    plt.clf()

if __name__=="__main__":
    read_from_file = False
    ksp_ks = [6, 8, 10]
    for params in [(36, 6)]:
        file_name = "ksp_" + str(params).replace(' ', '_')
        ksptput = defaultdict(defaultdict)
        if read_from_file:
            print "File not found."
        else:
            switch_k, num_servers_per_rack = params
            ksptput = ksp_tput_experiment(switch_k,
                                          num_servers_per_rack,
                                          ksp_ks)
            with open(file_name + '.json', 'w') as f:
                json.dump(ksptput, f)
        plot_all_all_tput(ksptput, file_name + ".pdf")
