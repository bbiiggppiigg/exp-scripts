import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
if len(sys.argv) < 2:
    print("Usage : expect 1 argument, filename of the usage file")
    exit(-1)

usage_file = sys.argv[1]
arch = usage_file[-10:-4]
#print(arch)
#exit(-1)
class MyException(Exception):
    pass



full = list()



sgpr_simple_reserve = list()
sgpr_extra_reserve = list()
sgpr_weird_reserve = list()

vgpr_simple_reserve = list()
vgpr_extra_reserve = list()
vgpr_weird_reserve = list()

def ecdf_values(x):
    """
    Generate values for empirical cumulative distribution function
    
    Params
    --------
        x (array or list of numeric values): distribution for ECDF
    
    Returns
    --------
        x (array): x values
        y (array): percentile values
    """
    
    # Sort values and find length
    x = np.sort(x)
    n = len(x)
    # Create percentiles
    y = np.arange(1, n + 1, 1) / n
    return x, y

def ecdf_plot(x, name = 'Value', plot_normal = True, log_scale=False, save=False, save_name='Default'):
    """
    ECDF plot of x

    Params
    --------
        x (array or list of numerics): distribution for ECDF
        name (str): name of the distribution, used for labeling
        plot_normal (bool): plot the normal distribution (from mean and std of data)
        log_scale (bool): transform the scale to logarithmic
        save (bool) : save/export plot
        save_name (str) : filename to save the plot

    Returns
    --------
        none, displays plot

    """
    xs, ys = ecdf_values(x)
    fig = plt.figure(figsize = (10, 6))
    ax = plt.subplot(1, 1, 1)
    plt.step(xs, ys, linewidth = 2.5, c= 'b');

    plot_range = ax.get_xlim()[1] - ax.get_xlim()[0]
    fig_sizex = fig.get_size_inches()[0]
    data_inch = plot_range / fig_sizex
    right = 0.6 * data_inch + max(xs)
    gap = right - max(xs)
    left = min(xs) - gap

    if log_scale:
        ax.set_xscale('log')

    if plot_normal:
        gxs, gys = ecdf_values(np.random.normal(loc = xs.mean(),
                                                scale = xs.std(),
                                                size = 100000))
        plt.plot(gxs, gys, 'g');

    plt.vlines(x=min(xs),
               ymin=0,
               ymax=min(ys),
               color = 'b',
               linewidth = 2.5)

    # Add ticks
    plt.xticks(size = 16)
    plt.yticks(size = 16)
    # Add Labels
    plt.xlabel(f'{name}', size = 18)
    plt.ylabel('Percentile', size = 18)

    plt.vlines(x=min(xs),
               ymin = min(ys),
               ymax=0.065,
               color = 'r',
               linestyle = '-',
               alpha = 0.8,
               linewidth = 1.7)

    plt.vlines(x=max(xs),
               ymin=0.935,
               ymax=max(ys),
               color = 'r',
               linestyle = '-',
               alpha = 0.8,
               linewidth = 1.7)

    # Add Annotations
    plt.annotate(s = f'{min(xs):.2f}',
                 xy = (min(xs),
                       0.065),
                horizontalalignment = 'center',
                verticalalignment = 'bottom',
                size = 15)
    plt.annotate(s = f'{max(xs):.2f}',
                 xy = (max(xs),
                       0.935),
                horizontalalignment = 'center',
                verticalalignment = 'top',
                size = 15)

    ps = [0.25, 0.5, 0.75]

    for p in ps:

        ax.set_xlim(left = left, right = right)
        ax.set_ylim(bottom = 0)

        value = xs[np.where(ys > p)[0][0] - 1]
        pvalue = ys[np.where(ys > p)[0][0] - 1]

        plt.hlines(y=p, xmin=left, xmax = value,
                    linestyles = ':', colors = 'r', linewidth = 1.4);

        plt.vlines(x=value, ymin=0, ymax = pvalue,
                   linestyles = ':', colors = 'r', linewidth = 1.4)

        plt.text(x = p / 3, y = p - 0.01,
                 transform = ax.transAxes,
                 s = f'{int(100*p)}%', size = 15,
                 color = 'r', alpha = 0.7)

        plt.text(x = value, y = 0.01, size = 15,
                 horizontalalignment = 'left',
                 s = f'{value:.2f}', color = 'r', alpha = 0.8);

    # fit the labels into the figure
    plt.title(f'ECDF of {name}', size = 20)
    plt.tight_layout()


    if save:
        plt.savefig(save_name + '.png')





def plot_data2(data1,data2,fname):
    fig,ax = plt.subplots()
    #labels, counts = np.unique(data1, return_counts=True)
    
    xs1, ys1 = ecdf_values(data1)
    #labels2, counts2 = np.unique(data2, return_counts=True)
    
    xs2, ys2 = ecdf_values(data2)
    #plt.bar(labels, counts, align='center')
    ax.ecdf(data1, label="With given allocation", complementary=True)
    ax.ecdf(data2, label="With increased allocation", complementary=True)
    
    x_threshold = 2
    yvalue1 = 1-ys1[np.where(xs1 > x_threshold)[0][0] ]
    yvalue2 = 1-ys2[np.where(xs2 > x_threshold)[0][0] ]
    print("yavlue = ",yvalue1,yvalue2)

    ax.hlines(y=yvalue1, xmin=0, xmax = x_threshold,
                linestyles = ':', colors = 'r', linewidth = 1.4);

    ax.hlines(y=yvalue2, xmin=0, xmax = x_threshold,
                linestyles = ':', colors = 'b', linewidth = 1.4);


    ax.vlines(x=x_threshold, ymin=0, ymax = max(yvalue1,yvalue2),
               linestyles = ':', colors = 'r', linewidth = 1.4)


    ax.text(x = 0, y = yvalue1 - 0.01,
                 transform = ax.transAxes,
                 s = f'{int(100*yvalue1)}%', size = 15,
                 color = 'r', alpha = 0.7)

    ax.text(x = 0, y = yvalue2 - 0.01,
                 transform = ax.transAxes,
                 s = f'{int(100*yvalue2)}%', size = 15,
                 color = 'b', alpha = 0.7)


    #ax.hist(np.array(data1)/sum(data1))
    #ax.hist(np.array(data2)/sum(data2))
    if "Scalar" in fname:
        ax.set_ylim([0,1.01])
        ax.set_xlim([0,16])
    else:
        ax.set_ylim([0,1.01])
        ax.set_xlim([0,10])
    #else:
    #    ax.set_xlim([0,256])
    #ax.hist(usage_list,bins=[x for x in range(1,16)])
    #if "extra" not in fname:
    #    ax.set_ylim([0,210])
    #    ax.set_xlim([0,16])
    #else:
    #    ax.set_ylim([0,140])
    #    ax.set_xlim([0,90])
    ax.grid(True)
    ax.legend()
    ax.set_xlabel(f"Number of Rerservable (Unused) {fname} Registers")
    ax.set_ylabel("Percentage of Kernels")
    ax.label_outer()

    plt.savefig(f"{fname}_{arch}.png")
    plt.close()


def plot_data(data,fname):
    usage_list = data
    fig,ax = plt.subplots()
    labels, counts = np.unique(usage_list, return_counts=True)
    #plt.bar(labels, counts, align='center')
    ax.ecdf(counts, label="CDF")
    #ax.hist(usage_list,bins=[x for x in range(1,16)])
    if "extra" not in fname:
    #    ax.set_ylim([0,210])
        ax.set_xlim([0,16])
    else:
    #    ax.set_ylim([0,140])
        ax.set_xlim([0,90])

    plt.savefig(f"{fname}_{arch}.png")
    plt.close()

threshold = 2
v_threshold = 2
def parse_line(line,lid):
    try:
        fname,kname,sgpr_parse,sgpr_note,sgpr_kd,vgpr_parse,vgpr_note,vgpr_kd,agpr_parse,agpr_note,agpr_kd = line.split(",")
        sgpr_parse = int(sgpr_parse)
        sgpr_kd = int(sgpr_kd)
        sgpr_note = int(sgpr_note)
        
        vgpr_parse = int(vgpr_parse)
        vgpr_kd = int(vgpr_kd)
        vgpr_note = int(vgpr_note)

        agpr_kd = int(agpr_kd)
        agpr_note = int(agpr_note)
        agpr_parse = int(agpr_parse)
        
        assert sgpr_parse <= sgpr_note and sgpr_note <= sgpr_kd , "sgpr inequality" 
        assert vgpr_parse <= vgpr_note and vgpr_note <= vgpr_kd , "vgpr inequality" 
        assert agpr_parse <= agpr_note and agpr_note <= agpr_kd , "agpr inequality"

        if(sgpr_kd %16):
            sgpr_kd -= 8
        assert (sgpr_kd &0xf) ==0 , "sgpr_kd should be multiples of 16"
        if vgpr_kd - vgpr_note >= v_threshold:
            vgpr_simple_reserve.append(vgpr_kd - vgpr_note)
        else:
            vgpr_simple_reserve.append(0)
        if vgpr_parse < vgpr_note:
            vgpr_weird_reserve.append(vgpr_kd - vgpr_parse)
        if 256 - vgpr_note >= v_threshold:
            vgpr_extra_reserve.append(256 - vgpr_note)
        else:
            vgpr_extra_reserve.append(0)

        #if sgpr_kd%16 != 0:
        #    raise MyException(sgpr_kd-8,sgpr_note)
        if sgpr_kd - sgpr_note >= threshold:
            sgpr_simple_reserve.append(sgpr_kd - sgpr_note)
        else:
            sgpr_simple_reserve.append(0)
        if sgpr_parse < sgpr_note and sgpr_note - sgpr_parse >2:
            if sgpr_kd - sgpr_parse - 6 > 0:
                sgpr_weird_reserve.append(sgpr_kd - sgpr_parse - 6)
        #    print(line)
        if 102 > sgpr_note:
            if 102 - sgpr_note >= threshold:
                sgpr_extra_reserve.append(102-sgpr_note)
        else:
            sgpr_extra_reserve.append(0)
        full.append(1) 
    except Exception as e:
        print("line = ",line)
        print("Exception",repr(e))

with open(usage_file) as f:
    lines = f.readlines()
    for lid in range(len(lines)):
        parse_line(lines[lid],lid)
    lsr = len(sgpr_simple_reserve)
    lrr = len(sgpr_extra_reserve)
    lsw = len(sgpr_weird_reserve)
    
    lvsr = len(vgpr_simple_reserve)
    lver = len(vgpr_extra_reserve)
    lvwr = len(vgpr_weird_reserve)

    lf  = len(full)
    #plot_data(sgpr_simple_reserve,"sgpr_simple_reserve")
    #plot_data(sgpr_extra_reserve,"sgpr_extra_reserve")

    #plot_data(vgpr_simple_reserve,"vgpr_simple_reserve")
    #plot_data(vgpr_extra_reserve,"vgpr_extra_reserve")
    plot_data2(sgpr_simple_reserve,sgpr_extra_reserve,"Scalar")
    plot_data2(vgpr_simple_reserve,vgpr_extra_reserve,"Vector")
    print("FILE NAME = ",usage_file)
    print(lsr,lrr,lf)
    print(lsr/lf,lrr/lf)
    print(lsw/lf)

    print(lvsr,lver,lf)
    print(lvsr/lf,lver/lf)
    print(lvwr/lf)
