#!//home/hw60/bin/conda/bin/python
import re
from statistics import stdev as stdev
from statistics import mean as mean

def parse_bline(line):
    try:
        res = re.match(r"(.*\(.*\)) bcount = (\d+): Elapsed duration = (\d+)",line)
        #print(res.group(1),res.group(2),res.group(3))
        return (res.group(1)),int(res.group(2)),int(res.group(3))
    except:
        print ("HA",line)
        exit(-1)
        pass


def parse_line(line):
    try:
        res = re.match(r"(.*\(.*\)) : Elapsed duration = (\d+)",line)
        #print(res.group(1),res.group(2))
        return res.group(1), int(res.group(2))
    except:
        parse_bline(line)
        pass

base_dict = dict()
instr_dict = dict()
bcount_dict = dict()

with open('out') as f:
    lines = f.readlines()
    l_len = len(lines)>>1
    
    print(l_len)
    base_lines = lines[:l_len]
    instr_lines = lines[l_len:]

    for bl in base_lines:
        kname, duration = parse_line(bl)
        if kname not in base_dict:
            base_dict[kname] = list()
            instr_dict[kname] = list()
        base_dict[kname].append(duration)

    for il in instr_lines:
        kname, bcount, duration = parse_bline(il)
        if kname not in bcount_dict:
            bcount_dict[kname] = bcount
        instr_dict[kname].append(duration)
    

for kname in base_dict:
    bcount = bcount_dict[kname]
    if bcount != 0:
        assert(len(base_dict[kname])%10==0)
        total = len(base_dict[kname])
        step = int(total/10)
        curr = 0
        while curr < total:
            #print(kname, bcount , mean(base_dict[kname][curr:curr+step]), stdev(base_dict[kname][curr:curr+step]),
            #        mean(instr_dict[kname][curr:curr+step]), stdev(instr_dict[kname][curr:curr+step]))
            print("%s %d %.0f %.0f"%(kname, bcount , mean(base_dict[kname][curr:curr+step]),
                mean(instr_dict[kname][curr:curr+step])))

            curr += step

        with open('%s.out'%kname,'w') as wf:
            for ii in range(len(base_dict[kname])):
                wf.write("%d %d\n"%(base_dict[kname][ii],instr_dict[kname][ii]))

