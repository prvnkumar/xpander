import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

mpl.rcParams['lines.linewidth'] = 4
mpl.rcParams['lines.markersize'] = 10
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.8
mpl.rcParams['legend.framealpha'] = 0.8
mpl.rcParams['figure.figsize'] = (7,4)

getcolor = {"xpander" : "gray",
            "jellyfish" : "orange",
            "opt" : "blue"}
getmarker = {"xpander" : "d",
             "jellyfish" : "<",
             "opt" : "x"}

def plot_path_lengths(path_lengths, file_name):
    plt.figure(figsize=(6,4))
    for topo_type, data in path_lengths.iteritems():
        num_servers = sorted([int(k) for k in data.keys()])
        path_lengths = [float(data[i]) for i in num_servers]
        print data
        plt.plot(num_servers, path_lengths,
                 color = getcolor[topo_type],
                 linestyle = '-',
                 marker = getmarker[topo_type],
                 label=topo_type)
    plt.xlabel("Number of servers")
    plt.ylabel("Avg. shortest paths")
    plt.legend(loc="best")
    plt.savefig(file_name)
    plt.clf()

def plot_all_all_tput(aa_tput, file_name):
    plt.figure(figsize=(6,4))
    for topo_type, data in aa_tput.iteritems():
        num_servers = sorted([int(k) for k in data.keys()])
        tput = [float(data[i]) for i in num_servers]
        print data
        plt.plot(num_servers, tput,
                 color = getcolor[topo_type],
                 linestyle = '-',
                 marker = getmarker[topo_type],
                 label=topo_type)
    plt.xlabel("Number of servers")
    plt.ylabel("Normalized throughput")
    plt.legend(loc="best")
    plt.savefig(file_name)
    plt.clf()

def plot_ksp_fail_tput(ksp_tput, file_name):
    plt.figure()
    for topo_type, data in ksp_tput.iteritems():
        fail_rates = sorted([float(k) for k in data.keys()])
        tput = [float(data[i]) for i in fail_rates]
        print data
        plt.plot(fail_rates, tput,
                 color = getcolor[topo_type],
                 linestyle = '-',
                 marker = getmarker[topo_type],
                 label=topo_type)
    plt.xlabel("Link failure rate")
    plt.ylabel("Normalized throughput")
    plt.ylim(0.1, 1.0)
    plt.legend(loc="best")
    plt.savefig(file_name)
    plt.clf()

