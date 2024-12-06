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
stepplot, = ax.step(outcomes.keys(), outcomes.values(), where='mid',color='blue')

new_data = False

def get_n_oc(oc):
    n=0
    v=oc.values()
    for x in v:
        n+=x
    return n

def do_plot():
    global new_data
    new_data=False
    
    global fig, ax, stepplot

    #update plot
    ocv = list(outcomes.values())
    max_y = get_max(ocv)+1
    ax.set_ylim(0,max_y);
    stepplot.set_ydata(ocv)
    
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
    new_data=True
    return web.Response(text="ok")

async def get_cats(req):
    j = json.dumps(possible_outcomes)
    return web.Response(text=j,content_type="application/json")

def web_runner():
    app = web.Application()
    static_path=os.path.join(script_path,"student")
    print(static_path)    
    app.add_routes([
        web.static('/', static_path),
        web.post('/outcome', add_outcome),
        web.get('/cats', get_cats)
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
