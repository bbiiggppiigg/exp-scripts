#!/usr/bin/python3

import sys
if(len(sys.argv) < 2):
    print("usage : ./analyze_raw.py <filename>")
    exit(-1)

infile = sys.argv[1]

lines = open(infile,"r").readlines()

def count_align_sgprs(sgpr_in):
    pairs = [ sgpr_in[x:x+2] for x in range(0,len(sgpr_in),2)  ]
    #print(pairs)
    return len(list(filter(lambda s : s == "00", pairs)))


def analyze_align_sgpr_pairs(lines,x_i,sgpr_claimed):
    num_lines = len(lines)
    min_pairs = sgpr_claimed
    first_addr = None
    ret  = []
    while x_i < num_lines:
        if lines[x_i].count(",") != 1:
            break
        addr,raw = lines[x_i].strip().split(",")
        sgpr = raw[512:]
        sgpr = sgpr[::-1]
        sgpr = sgpr[:sgpr_claimed]
        new_pair = count_align_sgprs(sgpr)
        ret.append(new_pair)
        min_pairs = min(min_pairs,new_pair)
        
        if first_addr is not None:
            first_addr = addr
        x_i = x_i + 1
    return x_i, min_pairs , "0x"+addr, ret

def process(lines):
    num_lines = len(lines)
    i = 0
    ret = []
    while i < num_lines:
        if lines[i].count(",") != 3 :
            break
        fname,kname,sgpr_claimed,vgpr_claimed = lines[i].split(",")
        sgpr_claimed = int(sgpr_claimed)

        i , min_pairs , addr , new_pairs = analyze_align_sgpr_pairs(lines,i+1,sgpr_claimed)
        #print(addr,min_pairs)
        ret += new_pairs

    for avail in range(1,max(ret)):
        pair_avail = len(list(filter(lambda x : x >= avail, ret)))
        print(" %d or more available even aligned sgpr pairs = %2f\n"%(avail , pair_avail / len(ret)))
process(lines)
