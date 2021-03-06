from xpander import *
from jellyfish import *
from routing import *

lift_k = 2
switch_d = 2
i = 3
num_servers = xpander_num_servers(1 << i, 1, switch_d, lift_k)
print num_servers

topo = Xpander(num_servers, 1, switch_d, draw=True,
               draw_output="incr_graphs/" + str(num_servers) + ".png",
               convert_to_topo=False)
jfTopo = Jellyfish(num_servers, 1, switch_d, draw=True,
                   draw_output="incr_graphs/" + str(num_servers) + "_jf.png",
                   convert_to_topo=False)

for j in range(100):
    num_servers += 1
    print num_servers

    # Draw every 10th 
    draw = bool(num_servers % 10 == 1)
    topo.add_one_node(draw=draw, draw_output="incr_graphs/" + str(num_servers + 1) + "_incr.png")
    jfTopo.add_one_node(draw=draw, draw_output="incr_graphs/" + str(num_servers +1) + "_jf_incr.png")
