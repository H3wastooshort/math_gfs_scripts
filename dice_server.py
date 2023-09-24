import asyncio
from aiohttp import web
from matplotlib import pyplot as plt
import numpy, matplotlib

possible_outcomes = range(1,7,1)
outcomes = {}
for o in possible_outcomes:
    outcomes[o] = 0

#set up plot
plt.ion()
plt.show()
fig,ax = plt.subplots()
stepplot, = ax.step(outcomes.keys(), outcomes.values(), where='mid')

new_data = True

def do_plot():
    global new_data
    new_data=False
    
    global stepplot, fig, ax
    ocv = list(outcomes.values())
    max_y = 0
    for y in ocv:
        if y > max_y:
            max_y = y+1
    ax.set_ylim(-1,max_y);
    stepplot.set_ydata(ocv)
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
        n=int(int)
    except:
        return web.Response(status=400,text="invalid outcome")
    if dat not in possible_outcomes:
        return web.Response(status=400,text="unknown outcome")
    outcomes[dat] += 1
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
server = loop.create_server(app.make_handler(), '127.0.0.1', 8000)
print("Server started at http://127.0.0.1:8000")
loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
