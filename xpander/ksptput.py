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
from alltput import *

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
            ksptput["opt"][ksp_k] = dict()

    switch_d = switch_k - num_servers_per_rack
    for num_servers in [num_servers_per_rack * (switch_d + 1) * (1 << i) for i in range(5)]:
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

        opt_aatput = aatput_ub(num_switches,
                               switch_d,
                               num_switches * (num_switches - 1))
        for ksp_k in ksp_ks:
            ksptput["opt"][ksp_k][num_servers] = opt_aatput

    return ksptput

if __name__=="__main__":
    read_from_file = False
    ksp_ks = [6, 8, 10]
    for params in [(36, 6)]:
        file_name = "output/ksp_tput_" + str(params).replace(' ', '_')
        ksptput = defaultdict(defaultdict)
        switch_k, num_servers_per_rack = params
        if read_from_file:
            try:
                tmp_len = None
                with open(file_name + '.json', 'r') as f:
                    tmp_len = json.load(f)
                for topo, data in tmp_len.iteritems():
                    ksptput[topo] = defaultdict(defaultdict)
                    for ksp_k,serv_tput in data.iteritems():
                        ksp_k = int(ksp_k)
                        ksptput[topo][ksp_k] = defaultdict(float)
                        for num_serv,tput in serv_tput.iteritems():
                            num_serv = int(num_serv)
                            tput = float(tput)
                            ksptput[topo][ksp_k][num_serv] = tput
            except IOError:
                print "File not found."
        else:
            ksptput = ksp_tput_experiment(switch_k,
                                          num_servers_per_rack,
                                          ksp_ks)
            with open(file_name + '.json', 'w') as f:
                json.dump(ksptput, f)
        plot.plot_ksp_tput(ksptput, file_name + ".png", num_servers_per_rack)
        plot.plot_ksp_tput(ksptput, file_name + ".png",
                           num_servers_per_rack, aggregate=True)
        plot.plot_ksp_tput(ksptput, file_name + ".png", num_servers_per_rack,
                           per_node=True)
