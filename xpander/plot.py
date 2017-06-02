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

def plot_ksp_tput(ksp_tput, file_name, servers_per_rack, aggregate=False,
                  per_node=False):
    f, axarr = plt.subplots(2, sharey=True)
    axindex = 0
    for topo_type, ksp_data in ksp_tput.iteritems():
        if topo_type == 'opt':
            continue
        ax = axarr[axindex]
        for ksp_k, data in sorted(ksp_data.iteritems()):
            print data
            num_servers = sorted([int(k) for k in data.keys()])
            tput = [float(data[i])/ksp_tput['opt'][ksp_k][i] for i in num_servers]
            if aggregate:
                tput = [num_server / servers_per_rack
                        * (num_server / servers_per_rack - 1)
                        * float(data[num_server]) for num_server in num_servers]
            elif per_node:
                tput = [(num_server / servers_per_rack - 1)
                        * float(data[num_server]) for num_server in num_servers]
            ax.plot(num_servers, tput,
                     color = (['r','g', 'b']*10)[ksp_k],
                     linestyle = (['-','-.', '--']*10)[ksp_k],
                     marker = getmarker[topo_type],
                     label=topo_type + " k=" + str(ksp_k),
                     linewidth=int(ksp_k)/2)
            ax.legend(loc="best")
        axindex += 1
    plt.xlabel("Number of servers")
    if per_node:
        file_name = file_name[:-4] + "_pernode" + file_name[-4:]
        plt.ylabel("Per node throughput")
    elif aggregate:
        file_name = file_name[:-4] + "_aggregate" + file_name[-4:]
        plt.ylabel("Aggregate throughput")
    else:
        plt.ylabel("Throughput")
        plt.gca().set_yscale("log", nonposy='clip')
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

