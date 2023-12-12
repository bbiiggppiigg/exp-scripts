#!/usr/bin/python3

import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axis import Axis

TABLE = dict()

KD_SGPR = dict()
KD_VGPR = dict()
def parse_usage(line):
    arr = line.split(",")
    filename = arr[0]
    kernelname = arr[1]
    note_sgpr = int(arr[2])
    note_vgpr = int(arr[3])
    kd_sgpr = int(arr[4])
    kd_vgpr = int(arr[5])
    if filename not in KD_SGPR:
        KD_SGPR[filename] = dict()
        KD_VGPR[filename] = dict()
    if kernelname not in KD_SGPR[filename]:
        KD_SGPR[filename][kernelname] = dict()
        KD_VGPR[filename][kernelname] = dict()
    KD_SGPR[filename][kernelname] = kd_sgpr
    KD_VGPR[filename][kernelname] = kd_vgpr

lid = 0
def parse_line(line):
    global lid
    lid += 1
    print("lid = ",lid)
    arr = line.split(",")
    #print(arr[0:4])
    filename = arr[0]
    kernelname = arr[1]
    max_sgpr = int(arr[2])
    max_vgpr = int(arr[3])
    per_addr_usage = arr[4:]
    assert(len(per_addr_usage)%3==0)
    bb_addr = per_addr_usage[0]
    try: 
        sgpr_usage = KD_SGPR[filename][kernelname]
        vgpr_usage = KD_VGPR[filename][kernelname]
    except:
        print(KD_SGPR[filename].keys())
        print(f"dict_keys(['{kernelname}'])")
    if filename not in TABLE:
        TABLE[filename] = dict()
    if kernelname not in TABLE[filename]:
        TABLE[filename][kernelname] = dict()
    if bb_addr not in TABLE[filename][kernelname]:
        TABLE[filename][kernelname][bb_addr] = dict()
        TABLE[filename][kernelname][bb_addr][0] = list()
        TABLE[filename][kernelname][bb_addr][1] = list()
        TABLE[filename][kernelname][bb_addr][2] = (sgpr_usage,vgpr_usage) 


    sgpr_avail = list()
    vgpr_avail = list()
    for x in range(0,len(per_addr_usage),3):
        line_sgpr = int(per_addr_usage[x+1])
        line_vgpr = int(per_addr_usage[x+2])
        sgpr_avail.append(max_sgpr - line_sgpr)
        vgpr_avail.append(max_vgpr - line_vgpr)

    TABLE[filename][kernelname][bb_addr][0].append(sgpr_avail)
    TABLE[filename][kernelname][bb_addr][1].append(vgpr_avail)
    #print(sgpr_avail)
    #plt.hist(sgpr_avail)
    #plt.show()
    
    pass

assert(len(sys.argv) >= 2)
infile = (sys.argv[1])
arch = infile[3:-4]
print("ARCH = ",arch)
s_maxs = []
s_starts = []
s_ends = []
v_maxs = []
v_starts = []
v_ends = []
with open(infile) as f:
    lines = f.readlines()
    for line in lines:
        try:
            s_max,s_start,s_end,v_max,v_start,v_end = line.strip().split(" ")
        except:
            continue
        s_maxs.append(int(s_max))
        s_starts.append(int(s_start))
        s_ends.append(int(s_end))
        v_maxs.append(int(v_max))
        v_starts.append(int(v_start))
        v_ends.append(int(v_end))

import itertools
fid = 0
kid = 0
from scipy.stats import norm

def plot_data(data,goal,filename):
    usage_list = data
    min_data = min(usage_list)
    max_data = max(usage_list)
    fig,ax = plt.subplots()

    mybins = [ 4*x for x in range(0,64) ] if 'v' in goal else [ 8 * x for x in range(0,14) ]
    myticks = [ 8 * x for x in range(0,14) ] + [102]  if 's' in goal else [ 16 * x for x in range(0,17)]
    nn, bins, patches = ax.hist(usage_list,bins=mybins)
    ax.set_ylim(bottom=0,top=400)
    ax.set_xticks(myticks)
    x_right = 256 if "v" in goal else 102
    tt = "V" if "v" in goal else "S"
    ax.set_xlim(left=0,right=x_right)
    ax.set_title(f"{arch} {filename}")
    ax.set_xlabel(f'# of {tt}GPR available')
    ax.set_ylabel('# of Basic Blocks',rotation=90)
    plt.savefig(f"bb_png/{goal}_{filename}.{arch}.png")
    plt.close()
    pass

plot_data(s_maxs,'s','max')
plot_data(s_starts,'s','start')
plot_data(s_ends,'s','end')
plot_data(v_maxs,'v','max')
plot_data(v_starts,'v','start')
plot_data(v_ends,'v','end')


exit(-1)
