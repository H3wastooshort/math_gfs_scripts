import sys
if len(sys.argv) != 3:
    quit("server.py <number of players> <poll set file>")

import asyncio, threading, math, json, os
from aiohttp import web
from matplotlib import pyplot as plt

script_path = os.path.dirname(os.path.realpath(__file__))
print(script_path)

possible_outcomes = []
with open(sys.argv[2],"r") as f:
    possible_outcomes=json.loads(f.read())

n_players = int(sys.argv[1])

outcomes = {}
def reset_outcomes(oc,po):
    for x in po:
        oc[x] = 0
reset_outcomes(outcomes,possible_outcomes)

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
ax.set_xticks(possible_outcomes)
ax.set_xlim(get_min(possible_outcomes),get_max(possible_outcomes));
ax.set_ylim(0,n_players);
#ax.set_ylabel("")
#ax.set_xlabel("")
bellcurve_xvals = possible_outcomes
bellcurve, = ax.plot(bellcurve_xvals,bellcurve_xvals,color='grey', visible=False)
stepplot, = ax.step(outcomes.keys(), outcomes.values(), where='mid',color='blue')
stddevline1, = ax.plot([0,0],[0,0],color='red', visible=False)
stddevline2, = ax.plot([0,0],[0,0],color='red', visible=False)
meanline, = ax.plot([0,0],[0,0],color='lime', visible=False)

new_data = False

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

def get_n_oc(oc):
    n=0
    v=oc.values()
    for x in v:
        n+=x
    return n

sqrt_2pi = math.sqrt(2*math.pi)
def normal_ish_dist(x, mean,stddev):
    if stddev == 0:
        return 0
    #(1/(stddev*sqrt_2pi))  *
    return pow(math.e, -pow((x-mean)/stddev, 2) / 2)
def do_plot():
    global new_data
    new_data=False
    
    global fig, ax, stepplot, mean, meanline, bellcurve
    mean, stddev = calc_mean_and_stddev(outcomes)

    #update plot
    ocv = list(outcomes.values())
    max_y = get_max(ocv)+1
    ax.set_ylim(0,max_y);
    stepplot.set_ydata(ocv)
    
    meanline.set_xdata([mean,mean])
    meanline.set_ydata([0,max_y])
    meanline.set_visible(True)
    stddevline1.set_xdata([mean+stddev,mean+stddev])
    stddevline1.set_ydata([0,max_y])
    stddevline1.set_visible(True)
    stddevline2.set_xdata([mean-stddev,mean-stddev])
    stddevline2.set_ydata([0,max_y])
    stddevline2.set_visible(True)
    
    bc_y = []
    for x in bellcurve_xvals:
        bc_y.append(normal_ish_dist(x, mean,stddev)*(max_y-1))
    bellcurve.set_ydata(bc_y)
    bellcurve.set_visible(True)
    
    fig.canvas.draw()
    fig.canvas.flush_events()

def plot_loop():
    global plt
    try:
        while True:
            if new_data:
                do_plot()
            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(0.1)
    except KeyboardInterrupt:
        quit()

async def add_outcome(req):
    global new_data
    dat = await req.text()
    n=0
    try:
        n=int(dat)
    except:
        return web.Response(status=400,text="invalid outcome")
    if n not in possible_outcomes:
        return web.Response(status=400,text="unknown outcome")
    outcomes[n] += 1
    print(outcomes)
    return web.Response(text="ok")

def web_runner():
    app = web.Application()
    app.add_routes([
        web.static('/', script_path+"/student"),
        web.post('/outcome', add_outcome)
    ])
    runner = web.AppRunner(app)
    return runner

def run_server(runner):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, 'localhost', 8001)
    loop.run_until_complete(site.start())
    loop.run_forever()

t = threading.Thread(target=run_server, args=(web_runner(),))
t.start()

plot_loop()
