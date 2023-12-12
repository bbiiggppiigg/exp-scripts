#!/usr/bin/python3

import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

TABLE = dict()
lid = 1 
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

def parse_line(line):
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
        addr = int(per_addr_usage[x],16)
        line_sgpr = int(per_addr_usage[x+1])
        line_vgpr = int(per_addr_usage[x+2])
        assert(max_sgpr >= line_sgpr)
        if max_vgpr < line_vgpr:
            print(filename,lid,"addr = %x"%addr,"max = ",max_vgpr,"line = ",line_vgpr)
        assert(max_vgpr >= line_vgpr)
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
usagefile = (sys.argv[2])
outfolder = infile[:-4]
with open(usagefile) as f:
    lines = f.readlines()
    for line in lines:
        parse_usage(line)


with open(infile) as f:
    lines = f.readlines()
    for line in lines:
        parse_line(line)
        lid += 1
        #break
import itertools
fid = 0
kid = 0
from scipy.stats import norm

def plot_data(data,goal,filename,start_addr, max_gpr_claimed):
    usage_list = data
    min_data = min(usage_list)
    max_data = max(usage_list)
    step = ((max_data - min_data)/20)
    step = 0.1 if step == 0 else step
    bins = sorted(list(np.arange(min_data,max_data+step, step))+[1,2,3,4,5])
    mu, std = norm.fit(usage_list)
    #print(usage_list)
    #print(bins)
    #print(mu,std)
    fig,ax = plt.subplots()
    #bins = list(range(20))
    #ax.hist(np.clip(usage_list,bins[0],bins[-1]))#,bins=list(range(20)))
    #ax.hist(np.clip(usage_list,0,20),bins='auto')
    ax.hist(usage_list,bins='auto')
    """
    xmin,xmax = plt.xlim()
    print(xmin,xmax)
    x = np.linspace(xmin,xmax,int(xmax-xmin))
    p = norm.pdf(x,mu,std)
    ax.plot(x,p,'k',linewidth=10)
    print(x,p,sum(p))
    """
    if "v" in goal:
        ax.set_title("file: %s, kern_addr = 0x%#x\nmin_%s_avail = %u, claimable %s = %u\n"%(filename,start_addr,goal,min_data,goal,256 - max_gpr_claimed))
    else:
        ax.set_title("file: %s, kern_addr = 0x%#x\nmin_%s_avail = %u, claimable %s = %u\n"%(filename,start_addr,goal,min_data,goal,102 - max_gpr_claimed))
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
   
    ax.set_xlabel(f'# of {goal} available')
    ax.set_ylabel('# of Instructions',rotation=90)
    plt.savefig(f"{outfolder}/{filename}.png")
    plt.close()
    pass

def plot_2d_data(sgpr_list,vgpr_list,filename,start_addr, max_sgpr_claimed , max_vgpr_claimed):
    hist, xedges, yedges = np.histogram2d(sgpr_list,vgpr_list)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    #print(xpos,ypos)
    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    ax.set_xlim(xpos[-1],xpos[0])
    min_sgpr = min(sgpr_list)
    min_vgpr = min(vgpr_list)
    ax.set_title("file: %s\nkern_addr = 0x%#x, min_sgpr_avail = %u, min_vgpr_avail = %u\n, sgpr claimable = %u, vgpr claimable = %u"%(filename,start_addr,min_sgpr,min_vgpr,102-max_sgpr_claimed, 256 - max_vgpr_claimed))
    ax.set_xlabel('# SGPR available')
    ax.set_ylabel('# VGPR available')
    ax.set_ylim(bottom=0)
    ax.set_xlim(right=0)
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel('# of Instructions',rotation=90)
    plt.savefig(f"{outfolder}/{filename}.png")
    plt.close()
    pass


total_sgpr_list = list()
total_vgpr_list = list()

empty_sgpr_kernels = set()
empty_vgpr_kernels = set()
# PER KERNEL
for filename in TABLE:
    fid += 1
    kid = 0
    for kernelname in TABLE[filename]:
        kid += 1
        #print(f"{fid}-{kid}")
        sgpr_list = list()
        vgpr_list = list()
        start_addr = min( list(map(lambda x: int(x,16),TABLE[filename][kernelname].keys())))
        max_sgpr_claimed, max_vgpr_claimed = TABLE[filename][kernelname]["0x%x"%start_addr][2]
        for bb_addr in TABLE[filename][kernelname]:
            sgpr_list += list(itertools.chain(TABLE[filename][kernelname][bb_addr][0]))[0]
            vgpr_list += list(itertools.chain(TABLE[filename][kernelname][bb_addr][1]))[0]

        total_sgpr_list += sgpr_list
        total_vgpr_list += vgpr_list

        if 0 in sgpr_list:
            empty_sgpr_kernels.add(f"{fid}-{kid}/0x%x"%start_addr)
        if 0 in vgpr_list:
            empty_vgpr_kernels.add(f"{fid}-{kid}/0x%x"%start_addr)

        #plot_data(sgpr_list,'sgpr',filename, start_addr , max_sgpr_claimed)
        #plot_data(vgpr_list,'vgpr',filename, start_addr , max_vgpr_claimed)
        #plot_2d_data(sgpr_list,vgpr_list,filename, start_addr , max_sgpr_claimed , max_vgpr_claimed)


#for avail in range(1,10):
#    sgpr_constrained = (len(list(filter(lambda sgpr_avail : sgpr_avail < avail, total_sgpr_list))) )
#    print(" %d or less sgpr available percentage = %2f\n"%(avail-1,sgpr_constrained * 1.0 / len(total_sgpr_list)))

#for avail in range(1,10):
#    vgpr_constrained = (len(list(filter(lambda vgpr_avail : vgpr_avail < avail, total_vgpr_list))) )
#    print(" %d or less vgpr available percentage = %2f\n"%(avail-1,vgpr_constrained * 1.0 / len(total_vgpr_list)))

total_join_list = list(zip(total_sgpr_list,total_vgpr_list))
print(total_sgpr_list[:5])
print(total_vgpr_list[:5])
print(total_join_list[:5])
total_len = len(total_join_list)
for s_min in range(1,15):
    out_str = []
    for v_min in range(1,15):
        constrained = len(list(filter(lambda x: x[0] < s_min and x[1] < v_min , total_join_list)))
        out_str.append("%.2f"%(constrained * 100.0 / total_len))
    print(",".join(out_str))
        

#plot_data(total_sgpr_list,'sgpr','total_sgpr', start_addr , max_sgpr_claimed)
#plot_data(total_vgpr_list,'vgpr','total_vgpr', start_addr , max_vgpr_claimed)
#plot_2d_data(total_sgpr_list,total_vgpr_list,'total_2d', start_addr , max_sgpr_claimed , max_vgpr_claimed)

