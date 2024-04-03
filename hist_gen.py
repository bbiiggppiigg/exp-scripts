#!/usr/bin/python3
import sys
TABLE = dict()
lid = 1 
KD_SGPR = dict()
KD_VGPR = dict()
KD_AGPR = dict()
from common import parse_usage,parse_line,plot_data,plot_2d_data
gen_detail = False
assert(len(sys.argv) >= 2)
infile = (sys.argv[1])
usagefile = (sys.argv[2])
outfolder = infile[:-4]

if len(sys.argv) >= 4:
    gen_detail = True
with open(usagefile) as f:
    lines = f.readlines()
    for line in lines:
        parse_usage(line,KD_SGPR,KD_VGPR,KD_AGPR)


with open(infile) as f:
    lines = f.readlines()
    for line in lines:
        parse_line(line,KD_SGPR,KD_VGPR,KD_AGPR,TABLE)
        lid += 1
        #break
import itertools
fid = 0
kid = 0



total_sgpr_list = list()
total_vgpr_list = list()
total_agpr_list = list()

empty_sgpr_kernels = set()
empty_vgpr_kernels = set()
empty_agpr_kernels = set()
# PER KERNEL
for filename in TABLE:
    fid += 1
    kid = 0
    for kernelname in TABLE[filename]:
        kid += 1
        sgpr_list = list()
        vgpr_list = list()
        agpr_list = list()

        start_addr = min( list(map(lambda x: int(x,16),TABLE[filename][kernelname].keys())))
        max_sgpr_claimed, max_vgpr_claimed, max_agpr_claimed = TABLE[filename][kernelname]["0x%x"%start_addr][3]
        for bb_addr in TABLE[filename][kernelname]:
            sgpr_list += list(itertools.chain(TABLE[filename][kernelname][bb_addr][0]))[0]
            vgpr_list += list(itertools.chain(TABLE[filename][kernelname][bb_addr][1]))[0]
            agpr_list += list(itertools.chain(TABLE[filename][kernelname][bb_addr][2]))[0]

        total_sgpr_list += sgpr_list
        total_vgpr_list += vgpr_list
        total_agpr_list += agpr_list

        if 0 in sgpr_list:
            empty_sgpr_kernels.add(f"{fid}-{kid}/0x%x"%start_addr)
        if 0 in vgpr_list:
            empty_vgpr_kernels.add(f"{fid}-{kid}/0x%x"%start_addr)
        if 0 in agpr_list:
            empty_agpr_kernels.add(f"{fid}-{kid}/0x%x"%start_addr)
        if gen_detail:
            print(f"{fid}-{kid}")
            plot_data(sgpr_list,'sgpr',f'sgpr/{fid}-{kid}', start_addr , max_sgpr_claimed, outfolder)
            plot_data(vgpr_list,'vgpr',f'vgpr/{fid}-{kid}', start_addr , max_vgpr_claimed, outfolder)
            plot_data(agpr_list,'agpr',f'agpr/{fid}-{kid}', start_addr , max_agpr_claimed, outfolder)
        #plot_2d_data(sgpr_list,vgpr_list,filename, start_addr , max_sgpr_claimed , max_vgpr_claimed, outfolder)

plot_data(total_sgpr_list,'sgpr','total_sgpr', start_addr , max_sgpr_claimed,outfolder,True)
plot_data(total_vgpr_list,'vgpr','total_vgpr', start_addr , max_vgpr_claimed,outfolder,True)
plot_data(total_agpr_list,'agpr','total_agpr', start_addr , max_agpr_claimed,outfolder,True)
#plot_2d_data(total_sgpr_list,total_vgpr_list,'total_2d', start_addr , max_sgpr_claimed , max_vgpr_claimed,outfolder)

