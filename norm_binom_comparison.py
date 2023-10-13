import asyncio, threading, math, scipy
from time import sleep
from matplotlib import pyplot as plt

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
def normal_dist_area(a,b,mu,sigma):
    B_a = scipy.stats.norm.cdf(a,loc=mu,scale=sigma)
    B_b = scipy.stats.norm.cdf(b,loc=mu,scale=sigma)
    return B_b - B_a
def draw_bars(n,pp):
    ##calc
    p=pp/100
    bars_norm={}
    bars_binom={}
    mu=n*p
    sigma=math.sqrt(n*p*(1-p))
    for k in range(n+1):
        bars_binom[k] = scipy.stats.binom.pmf(k,n,p)
        bars_norm[k] = normal_dist_area(k-0.5,k+0.5,mu,sigma)
    ##draw (badly)
    text="n=%d\np=%0.2f\nµ=%0.2f\nσ=%0.2f"%(n,p,mu,sigma)
    ax.clear()
    ax.set_ylabel("P")
    ax.set_xlabel("k")
    #ax.set_xticks(range(n+1))
    ax.bar(x=list(bars_binom.keys()),height=bars_binom.values(),width=1, align='center',edgecolor='red',color='mistyrose', alpha= 0.5)
    ax.bar(x=list(bars_norm.keys()),height=bars_norm.values(),width=1, align='center',edgecolor='blue',color='lightblue', alpha= 0.5)
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
