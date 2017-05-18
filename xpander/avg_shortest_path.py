from xpander import *
from routing import *

NUM_SERVERS = 256
NUM_SERVERS_PER_RACK = 4 # NUM_SWITCHES = NUM_HOSTS / NUM_SERVERS_PER_RACK

def find_avg_shortest_path():
    topo = Xpander(NUM_SERVERS, NUM_SERVERS_PER_RACK, switch_d=7, lift_k=8).G
    routing = Routing(topo)
    paths = routing.ksp(1)
    avg_shortest_path = 0.0
    num_paths = 0.0
    for s in topo.nodes_iter():
        for d in topo.nodes_iter():
            if s != d:
                min_path_len = len(paths[s][d][0])
                avg_shortest_path += min_path_len
                num_paths += 1 
                
    print "Avg shortest path: %.4f" % (avg_shortest_path / num_paths)

if __name__=="__main__":
    find_avg_shortest_path()
