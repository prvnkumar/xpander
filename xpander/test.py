from xpander import *
from routing import *

def test1():
    topo = Xpander(256, 4, switch_d=7, lift_k=8).G
    routing = Routing(topo)
    paths = routing.ksp(4)
    for s in topo.nodes_iter():
        for d in topo.nodes_iter():
            if s != d:
                print s, d, paths[s][d]


if __name__=="__main__":
    test1()
