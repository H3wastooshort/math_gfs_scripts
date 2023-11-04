import asyncio, threading, math, scipy
from time import sleep
from matplotlib import pyplot as plt

graph_sigma=0.5

#set up plot
plt.rc('axes', labelsize='x-large', titlesize='xx-large')
plt.rc('xtick', labelsize='x-large')
plt.rc('ytick', labelsize='x-large')
plt.rc('legend', fontsize='xx-large')
plt.ion()
plt.show()
fig,ax = plt.subplots()

def plot_done():
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.flush_events()
    print("plot completed")
graph_width=graph_sigma*5
def draw_bars(n): #something causes errors here, idk what \(°-°)/
    ##calc
    bars={}
    bar_width = graph_width/n
    for i in range(-n,n):
        x = i * bar_width
        bars[x] = scipy.stats.norm.pdf(x+(bar_width/2),loc=0,scale=graph_sigma)
    text="P="+str(scipy.stats.norm.pdf(0,loc=0,scale=graph_sigma) * bar_width)
    ##draw (badly)
    ax.clear()
    ax.bar(x=list(bars.keys()),height=bars.values(),width=bar_width, align='edge',edgecolor='blue',color='lightblue')
    ax.annotate(text, xy=(bar_width,bars[0]),textcoords='axes fraction',va='top', ha='right',xytext=(0.95,0.95), fontsize='xx-large', arrowprops=dict(facecolor='black', shrink=0.05))
    ax.set_xlim(-graph_width,graph_width)
    plot_done()

last_n=-1
def input_loop():
    global last_n
    while True:
        inp=input("Enter n/2 of bars: ")
        if inp == 'q':
            quit()
        if inp.isdigit():
            last_n=int(inp)
        else:
            print("numbers only pls")

input_thread = threading.Thread(target=input_loop)
input_thread.start()

while True:
    if last_n > 0:
        draw_bars(last_n)
        last_n=-1
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.start_event_loop(0.1)
