import asyncio, threading, math
from time import sleep
from scipy import stats
from matplotlib import pyplot as plt

graph_p = 0.6

#set up plot
plt.ion()
plt.show()
fig,ax = plt.subplots()
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
#ax.set_ylabel("")
#ax.set_xlabel("")

def draw_bars(n):
    ##calc
    bars={}
    bar_width = 1/n
    for k in range(0,n):
        bars[k/n]= stats.binom.pmf(k,n,graph_p)
    #text="P="+str(stats.binom.pmf(k,0,graph_p))
    ##draw (badly)
    ax.clear()
    ax.bar(x=list(bars.keys()),height=bars.values(),width=bar_width, align='edge',edgecolor='blue',color='lightblue')
    #ax.annotate(text, xy=(bar_width,bars[0]),textcoords='axes fraction',va='top', ha='right',xytext=(0.95,0.95), fontsize='xx-large', arrowprops=dict(facecolor='black', shrink=0.05))

def input_loop():
    while True:
        inp=input("Enter n of bars: ")
        if inp == 'q':
            quit()
        draw_bars(int(inp))

input_thread = threading.Thread(target=input_loop)
input_thread.start()

while True:
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.start_event_loop(0.1)
