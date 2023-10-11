import asyncio, threading, math, scipy
from time import sleep
from matplotlib import pyplot as plt

graph_sigma=0.5
graph_width=graph_sigma*3

#set up plot
plt.ion()
plt.show()
fig,ax = plt.subplots()
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
#ax.set_ylabel("")
#ax.set_xlabel("")

def normal_dist_area(a,b):
    B_a = scipy.stats.norm.cdf(a,loc=0,scale=graph_sigma)
    B_b = scipy.stats.norm.cdf(b,loc=0,scale=graph_sigma)
    return B_b - B_a

def plot_done():
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.flush_events()
    print("plot completed")
def draw_bars(n): #something causes errors here, idk what \(°-°)/
    ##calc
    bars={}
    bar_width = graph_width/n
    for i in range(0,n):
        x = i * bar_width
        bars[x] = normal_dist_area(x,x+bar_width)
    text="P="+str(normal_dist_area(0,bar_width))
    ##draw (badly)
    ax.clear()
    ax.bar(x=list(bars.keys()),height=bars.values(),width=bar_width, align='edge',edgecolor='blue',color='lightblue')
    ax.annotate(text, xy=(bar_width,bars[0]),textcoords='axes fraction',va='top', ha='right',xytext=(0.95,0.95), fontsize='xx-large', arrowprops=dict(facecolor='black', shrink=0.05))
    ax.set_xlim(0,graph_width)
    plot_done()

def input_loop():
    while True:
        inp=input("Enter n of bars: ")
        if inp == 'q':
            quit()
        if inp.isdigit():
            draw_bars(int(inp))
        else:
            print("numbers only pls")

input_thread = threading.Thread(target=input_loop)
input_thread.start()

plt.gcf().canvas.start_event_loop()
