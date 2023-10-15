import math, sys
from matplotlib import pyplot as plt

outcomes = []


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


fig,ax = plt.subplots()
#ax.set_ylabel("")
#ax.set_xlabel("")
ax.step(even_summier_sum_outcomes.keys(), even_summier_sum_outcomes.values(), where='mid',color='blue')
ax.annotate("",xycoords='axes fraction', xy=(0.05,0.95), va='top', ha='left', fontsize='xx-large')

plt.show()
