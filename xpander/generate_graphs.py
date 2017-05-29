from xpander import *
from routing import *

lift_k = 2
for switch_d in [2, 3]:
    for i in range(2, 10):
        num_servers = xpander_num_servers(1 << i, 1, switch_d, lift_k)
        if num_servers == None:
            continue
        print num_servers
        topo = Xpander(num_servers, 1, switch_d, draw=True,
                       draw_output="graphs/" + str(num_servers) + ".png").G
