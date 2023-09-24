import asyncio, threading
from aiohttp import web
from matplotlib import pyplot as plt
import numpy, matplotlib

outcomes_per_sum = 5

possible_outcomes = range(1,7,1)
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

possible_sum_outcomes = range(get_min(possible_outcomes)*outcomes_per_sum,(get_max(possible_outcomes)*outcomes_per_sum)+1,1)
sum_outcomes = {}
def reset_outcomes(oc,po):
    for x in po:
        oc[x] = 0
reset_outcomes(sum_outcomes,possible_sum_outcomes)

#set up plot
plt.ion()
plt.show()
fig,ax = plt.subplots()
stepplot, = ax.step(sum_outcomes.keys(), sum_outcomes.values(), where='mid')

new_data = True

def do_plot():
    global new_data
    new_data=False
    
    global stepplot, fig, ax
    sum_ocv = list(sum_outcomes.values())
    max_y = get_max(sum_ocv)+1
    ax.set_ylim(0,max_y);
    stepplot.set_ydata(sum_ocv)
    fig.canvas.draw()
    fig.canvas.flush_events()

def plot_loop():
    global plt
    while True:
        if new_data:
            do_plot()
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(0.1)

def do_outcome_sum():
    global new_data
    n=0
    for v in outcomes.values():
        n+=v
    if n >= outcomes_per_sum:
        #calc new sum and add to dist
        o_sum = 0
        for k in outcomes.keys():
            o_sum += k*outcomes[k]
            outcomes[k]=0
        print(o_sum)
        sum_outcomes[o_sum] += 1
    new_data=True
        

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
    do_outcome_sum()
    return web.Response(text="ok")

def web_loop():
    app = web.Application()
    app.add_routes([
        web.static('/', "student"),
        web.post('/outcome', add_outcome)
    ])
    web.run_app(app)

web_thread = threading.Thread(target=web_loop)
web_thread.start()

plot_loop()
