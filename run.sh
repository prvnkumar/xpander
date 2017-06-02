#!/bin/bash
python xpander/generate_graphs.py &
python xpander/avg_shortest_path.py &
python xpander/kspfailure.py &
python xpander/ksptput.py
