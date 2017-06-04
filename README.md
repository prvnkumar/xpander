# CS 244 '17: Reproducing Network Research
## Paper: Xpander: Towards Optimal-Performance Datacenters. CoNEXT ’16

Instructions to replicate
-------------------------

1. Set up a Google cloud instance, following the instructions here: https://cloud.google.com/compute/docs/quickstart-linux. Note that you will want a machine with at least four processors for reasonable performance as well as (ideally) at least 48GB of RAM. We recommend using either Debian or Ubuntu, though any Linux distribution should work.
2. The source code for our experiments is at https://github.com/prvnkumar/xpander.
3. Install the dependencies by running [download_deps.sh](download_deps.sh). See requirements below if not running on a supported architecture.
4. Start the virtual environment using source venv/bin/activate from the outermost directory of the repo.
5. To regenerate the graphs, just run the script [./run.sh](run.sh). This may take an hour or two depending on the hardware.
6. The data and graphs will be generated in the output/, graphs/ and incr_graphs/ directories, respectively.

Requirements
------------

If you want to run on a slightly different architecture, you will need the following:
* Python 2.7.X (tested with 2.7.9)
* Matplotlib (version 2.0.2, important!)
* Mininet
* PuLP (a Python linear equation solver)
* Networkx
* Standard Python libraries (math, numpy, random)
