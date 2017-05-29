import json
import math
import plot

from collections import defaultdict
from jellyfish import *
from routing import *
from xpander import *

LIFT_K = 2

def avgsp_lb(N, r):
    k = 1
    R = float(N - 1)
    for j in range(1, N):
        tmpR = R - (r * math.pow(r - 1, j - 1))
        if tmpR >= 0:
            R = tmpR
        else:
            k = j
            break
    opt_d = 0.0
    for j in range(1, k):
        opt_d += j * r * math.pow(r - 1, j - 1)
    opt_d += k * R
    opt_d /= (N - 1)
    return opt_d

def find_avg_shortest_path_host(topo, servers_per_rack):
    """Average inter-host shortest path length"""
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

def find_avg_shortest_path_sw(topo):
    """Average inter-switch shortest path length"""
    # Defining path length as the number of intermediate links
    routing = Routing(topo)
    paths = routing.ksp(1)
    avg_shortest_path = 0.0
    num_paths = 0.0
    for s in topo.nodes_iter():
        for d in topo.nodes_iter():
            if s != d:
                min_path_len = len(paths[s][d][0]) - 1
                avg_shortest_path += min_path_len
                num_paths += 1
    avg_shortest_path = avg_shortest_path / num_paths
    return avg_shortest_path

def avg_path_length_experiment(switch_k, num_servers_per_rack):
    splengths = defaultdict(defaultdict) # topo_type -> num_servers -> path_len
    switch_d = switch_k - num_servers_per_rack
    for num_servers in [(1 << i) for i in range(8, 15)]:
        # Might not get the exact number of servers as specified
        num_servers = xpander_num_servers(num_servers, num_servers_per_rack,
                                          switch_d, LIFT_K)
        if num_servers is None:
            continue
        print "num_servers: ", num_servers
        x_topo = Xpander(num_servers, num_servers_per_rack, switch_d=switch_d,
                         lift_k=LIFT_K).G
        j_topo = Jellyfish(num_servers, num_servers_per_rack, switch_d).G

        splengths["xpander"][num_servers] = nx.average_shortest_path_length(x_topo)
        splengths["jellyfish"][num_servers] = nx.average_shortest_path_length(j_topo)
        num_switches = num_servers / num_servers_per_rack
        splengths["opt"][num_servers] = avgsp_lb(num_switches, switch_d)
    return splengths

if __name__=="__main__":
    read_from_file = False
    for params in [(32,8), (48,12)]:
        file_name = "output/sp_" + str(params).replace(' ', '_')
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
        plot.plot_path_lengths(splengths, file_name + ".pdf")
