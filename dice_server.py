import asyncio, threading, math
from matplotlib import pyplot as plt

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

#set up plot
plt.ion()
plt.show()
fig,ax = plt.subplots()
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
#ax.set_ylabel("")
#ax.set_xlabel("")

sqrt_2pi = math.sqrt(2*math.pi)
def normal_dist(x, mean,stddev):
    if stddev == 0:
        return 0
    return (1/(stddev*sqrt_2pi))  *  pow(math.e, -pow((x-mean)/stddev, 2) / 2)

def normal_dist_area(start,stop):
    return 1

def do_iter(i):
    #calc
    bars={}
    bar_width = 1/i
    for n in range(0,i):
        x = n*bar_width
        bars[x]=normal_dist(x+(bar_width/2),0,0.25)# not real integral, should be width-root of integral
    text="A="+str(bars[0]*bar_width) # not real integral, whatever
    #draw (badly)
    ax.clear()
    ax.bar(x=list(bars.keys()),height=bars.values(),width=bar_width, align='edge',edgecolor='blue',color='lightblue')
    ax.annotate(text, xy=(bar_width,bars[0]),textcoords='axes fraction',va='top', ha='right',xytext=(0.95,0.95), fontsize='xx-large', arrowprops=dict(facecolor='black', shrink=0.05))

iteration=1
while True:
    do_iter(iteration)
    iteration += 1
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.start_event_loop(0.5)
