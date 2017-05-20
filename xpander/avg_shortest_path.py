import matplotlib as mpl
mpl.use('Agg')
import json
import math
import matplotlib.pyplot as plt

from collections import defaultdict
from jellyfish import *
from routing import *
from xpander import *

LIFT_K = 2

def find_avg_shortest_path(topo, topo_type, servers_per_rack):
    # Defining path length as the number of intermediate switches
    routing = Routing(topo)
    paths = routing.ksp(1)
    avg_shortest_path = 0.0
    num_paths = 0.0
    # Group all the servers in a rack together as the path is decided by
    # inter-switch graph
    for s in topo.nodes_iter():
        for d in topo.nodes_iter():
            if s != d:
                num_server_pairs = servers_per_rack * servers_per_rack
                min_path_len = len(paths[s][d][0])
                avg_shortest_path += min_path_len * num_server_pairs
                num_paths += num_server_pairs
            else:
                # if servers are in the same rack, path length = 1
                num_server_pairs = servers_per_rack * (servers_per_rack - 1)
                avg_shortest_path += 1 * num_server_pairs
                num_paths += num_server_pairs

    avg_shortest_path = avg_shortest_path / num_paths
    return avg_shortest_path

def avg_path_length_experiment(switch_k, num_servers_per_rack):
    splengths = defaultdict(defaultdict) # topo_type -> num_servers -> path_len
    switch_d = switch_k - num_servers_per_rack
    for num_servers in [256, 512, 1024, 2048, 4096, 8192, 16384]:
        num_switches = int(math.ceil(num_servers/num_servers_per_rack))
        if num_switches <= switch_d:
            continue

        # We might not get the exact number of servers specified
        num_lifts = int(math.ceil(math.log(num_switches/(switch_d+1), LIFT_K)))
        num_servers = int(num_servers_per_rack * (switch_d + 1) * math.pow(LIFT_K, num_lifts))
        print "num_servers: ", num_servers

        x_topo = Xpander(num_servers, num_servers_per_rack, switch_d=switch_d, lift_k=LIFT_K).G
        j_topo = Jellyfish(num_servers, num_servers_per_rack, switch_d).G

        splengths["xpander"][num_servers] = find_avg_shortest_path(x_topo,
                                                                 "Xpander",
                                                                 num_servers_per_rack)
        splengths["jellyfish"][num_servers] = find_avg_shortest_path(j_topo,
                                                                   "Jellyfish",
                                                                   num_servers_per_rack)
    return splengths

getcolor = {"xpander" : "gray", "jellyfish" : "orange"}
getmarker = {"xpander" : "o", "jellyfish" : "s"}

def plot_path_lengths(path_lengths, file_name):
    plt.figure(figsize=(6,4))
    for topo_type, data in path_lengths.iteritems():
        num_servers = sorted([int(k) for k in data.keys()])
        path_lengths = [float(data[i]) for i in num_servers]
        print data
        plt.plot(num_servers, path_lengths,
                 color = getcolor[topo_type],
                 linestyle = '-',
                 linewidth=4,
                 markersize=8,
                 marker = getmarker[topo_type],
                 label=topo_type)
    plt.xlabel("Number of servers")
    plt.ylabel("Avg. shortest paths")
    plt.legend(loc="best")
    plt.savefig(file_name)
    plt.clf()

if __name__=="__main__":
    read_from_file = True
    for params in [(32,8), (48,12)]:
        file_name = "sp_" + str(params).replace(' ', '_')
        splengths = defaultdict(defaultdict)
        if read_from_file:
            try:
                tmp_len = None
                with open(file_name + '.json', 'r') as f:
                    tmp_len = json.load(f)
                for topo, data in tmp_len.iteritems():
                    for k,v in data.iteritems():
                        splengths[topo][int(k)] = float(v)
            except IOError:
                print "File not found."
        else:
            switch_k, num_servers_per_rack = params
            splengths = avg_path_length_experiment(switch_k,
                                                   num_servers_per_rack)
            with open(file_name + '.json', 'w') as f:
                json.dump(splengths, f)
        plot_path_lengths(splengths, file_name + ".pdf")
