import math, sys
from matplotlib import pyplot as plt

outcomes = []
#read file
filenames=sys.argv
filenames.pop(0)
print("reading %d files..." % (len(filenames)))
for fn in filenames:
    f = open(fn,'r')
    for line in f:
        line = line.replace(',','.') #some stuff uses , instead of . as decimal seperators
        #print(line)
        try:
            outcomes.append(float(line))
        except ValueError:
            pass
    f.close()

print("sorting list...")
outcomes.sort()
oc_len = len(outcomes)
#print(outcomes)

def get_max(l):
    max_x = l[0]
    for x in l:
        if x > max_x:
            max_x = x
    return max_x
def get_min(l):
    min_x = l[0]
    for x in l:
        if x < min_x:
            min_x = x
    return min_x

def calc_mean_and_stddev(oc):
    n_oc = 0
    for v in oc.values():
        n_oc += v
    if n_oc < 1:
        return (0, 1)
    p_oc = {}
    mean = 0
    for k in oc.keys():
        p = (oc[k] / n_oc)
        p_oc[k] = p
        mean += p * k
    variance = 0
    for k in oc.keys():
        variance += p_oc[k] * pow(k - mean, 2)
    stddev = math.sqrt(variance)
    return (mean, stddev)

def nth_root(x,n):
    try:
        return x ** (1/n)
    except OverflowError:
        return 0

#calc stuff
print("calculating...")
bars_x=[]
bars_y=[]
bars_w=[]
for idx,this_oc in enumerate(outcomes):
    if idx==oc_len-1:
        break
    
    bars_x.append(this_oc)
    
    next_oc = outcomes[idx+1]
    width = next_oc - this_oc
    bars_w.append(width)
    
    probability_density=1
    
    bars_y.append(probability_density)

print(bars_x)
print(bars_y)
print(bars_w)

print("plotting...")

#do plot
fig,ax = plt.subplots()
#ax.set_ylabel("")
#ax.set_xlabel("")
ax.bar(bars_x, bars_y, bars_w, align='edge',edgecolor='blue',color='lightblue')
ax.annotate("",xycoords='axes fraction', xy=(0.05,0.95), va='top', ha='left', fontsize='xx-large')

plt.show()
