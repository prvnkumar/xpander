#!/bin/bash
python xpander/generate_graphs.py &
python xpander/avg_shortest_path.py &
python xpander/kspfailure.py &
python xpander/ksptput.py &
python xpander/generate_incr_graphs.py &
python xpander/alltput.py &
python xpander/alltput_incr.py &
