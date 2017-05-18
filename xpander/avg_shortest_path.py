from jellyfish import *
from routing import *
from xpander import *

#NUM_SERVERS = 256
NUM_SERVERS_PER_RACK = 8 # Given in the paper; NUM_SWITCHES = NUM_HOSTS / NUM_SERVERS_PER_RACK
SWITCH_D = 7

def find_avg_shortest_path(topo, topo_type):
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
                
    print "\tAvg shortest path for %s: %.4f" % (topo_type, avg_shortest_path / num_paths)

if __name__=="__main__":
    for num_servers in [128, 256, 512, 1024] + [1024*i for i in xrange(2, 3)]: #TODO: Want to go further but my VM gets sad for largr inputs
	    print ("Num servers: %d" % num_servers)

	    x_topo = Xpander(num_servers, NUM_SERVERS_PER_RACK, switch_d=SWITCH_D, lift_k=8).G
	    j_topo = Jellyfish(num_servers, NUM_SERVERS_PER_RACK).G
	    
	    find_avg_shortest_path(x_topo, "Xpander")
	    find_avg_shortest_path(j_topo, "Jellyfish")
