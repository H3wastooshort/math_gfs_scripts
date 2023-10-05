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
    bx=[]
    bw=[]
    bh=[]
    bar_width = 1/i
    for n in range(0,i+1,1):
        x = n/bar_width
        bx[n]=x
        bw[n]=bar_width
        bh[n]=normal_dist_area(x,x+bar_width)

    #draw (badly)
    ax.clear()
    barplot, = ax.bar(bx,bh,bw, align='left',color='blue')

iteration=0
while True:
    do_iter(iteration++)
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.start_event_loop(0.5)
