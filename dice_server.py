import asyncio
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
    max_x = 0
    for x in l:
        if x > max_x:
            max_x = x
    return max_x

possible_sum_outcomes = range(1,(get_max(possible_outcomes)*outcomes_per_sum)+1,1)
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
        
        #draw plot
        sum_ocv = list(sum_outcomes.values())
        max_y = get_max(sum_ocv)+1
        ax.set_ylim(0,max_y);
        stepplot.set_ydata(sum_ocv)
        fig.canvas.draw()
        fig.canvas.flush_events()

async def plot_loop():
    global plt
    while True:
        if new_data:
            do_plot()
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(0.1)
        await asyncio.sleep(0.1)

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
    new_data=True
    print(outcomes)
    return web.Response(text="ok")

#setup loop
loop = asyncio.get_event_loop()
loop.create_task(plot_loop())

#start webserver
app = web.Application(loop=loop)
app.add_routes([
    web.static('/', "student"),
    web.post('/outcome', add_outcome)
])
server = loop.create_server(app.make_handler(), '0.0.0.0', 8000)
print("Server started")
loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
