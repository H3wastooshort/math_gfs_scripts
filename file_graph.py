import math, sys
from matplotlib import pyplot as plt

outcomes_raw = []
min_width=float(input("enter min width: "))
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
            outcomes_raw.append(float(line))
        except ValueError:
            pass
    f.close()

print("sorting list...")
outcomes_raw.sort()

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

def calc_mean_and_stddev(lst):
    n_oc = len(lst)
    if n_oc < 1:
        return (0, 1)
    p_oc = {}
    mean = 0
    for v in lst:
        mean+=v
    mean /= n_oc
    
    variance = 0
    for v in lst:
        variance += pow(v - mean, 2)
    stddev = math.sqrt(variance/n_oc)
    return (mean, stddev)

def get_between(array,a,b):
    res=[]
    for x in array:
        if a<=x<=b:
            res.append(x)
    return len(res)

def nth_root(x,n):
    try:
        return x ** (1/n)
    except OverflowError:
        return 0

#calc stuff
print("calculating avg...")
outcomes=[]
for idx in range(math.floor(len(outcomes_raw)/5)):
    s=0
    for i in range(idx,idx+5):
        s+=outcomes_raw[i]
    outcomes.append(s)

oc_len = len(outcomes)

def find_next_idx(lst,start_idx,target):
    i = start_idx
    lst_len = len(lst)
    while i < lst_len:
        if lst[i]>=target:
            return i
        i+=1
    return -1

print("calculating plot...")
bars_x=[]
bars_y=[]
bars_w=[]
idx=0
raw_oc_len=len(outcomes_raw)
while True:
    this_oc=outcomes_raw[idx]
    
    bars_x.append(this_oc)
    
    next_oc = outcomes_raw[idx+1]
    width = max(min_width, next_oc - this_oc)
    bars_w.append(width)
    
    n_hits = get_between(outcomes_raw, this_oc, this_oc+width)
    
    bars_y.append(n_hits/width)
    
    idx=find_next_idx(outcomes_raw,idx,this_oc+width)
    if idx == -1:
        break
    if idx+1 >= raw_oc_len:
        break

print(bars_x)
print(bars_y)
print(bars_w)

print("calulating stats...")
mean, stddev = calc_mean_and_stddev(outcomes_raw)

print("plotting...")

#do plot
fig,ax = plt.subplots()
#ax.set_ylabel("")
#ax.set_xlabel("")
ax.bar(bars_x, bars_y, bars_w, align='edge',edgecolor='blue',color='lightblue')
ax.annotate("µ=%5f\nσ=%5f"%(mean,stddev),xycoords='axes fraction', xy=(0.05,0.95), va='top', ha='left', fontsize='xx-large')

print("showing plot...")
plt.show()
