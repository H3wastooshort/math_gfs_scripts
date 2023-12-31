import asyncio, threading, math, scipy
from time import sleep
from matplotlib import pyplot as plt

#set up plot
plt.rcParams.update({'font.size': 24})
#plt.rc('axes', labelsize='xx-large', titlesize='xx-large')
#plt.rc('xtick', labelsize='xx-large')
#plt.rc('ytick', labelsize='xx-large')
#plt.rc('legend', fontsize='xx-large')
plt.ion()
plt.show()
fig,ax = plt.subplots()

def plot_done():
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.flush_events()
    print("plot completed")
def draw_bars(n,pp):
    ##calc
    p=pp/100
    bars={}
    for k in range(n+1):
        bars[k] = scipy.stats.binom.cdf(k,n,p)
    ##draw (badly)
    text="n=%d\np=%0.2f"%(n,p)
    ax.clear()
    ax.set_ylabel("P")
    ax.set_xlabel("k")
    ax.set_xticks(range(n+1))
    ax.bar(x=list(bars.keys()),height=bars.values(),width=1, align='center',edgecolor='blue',color='lightblue')
    ax.annotate(text, xy=(0.95,0.95), xycoords='axes fraction',va='top', ha='right', fontsize='xx-large', arrowprops=dict(facecolor='black', shrink=0.05))
    plot_done()

def input_loop():
    while True:
        n=input("Enter n: ")
        pp=input("Enter p%: ")
        if 'q' in [n,pp]:
            quit()
        if n.isdigit() and pp.isdigit():
            draw_bars(int(n),int(pp))
        else:
            print("numbers only pls")

input_thread = threading.Thread(target=input_loop)
input_thread.start()

plt.gcf().canvas.start_event_loop()
