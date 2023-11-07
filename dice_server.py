import asyncio, threading, math
from aiohttp import web
from matplotlib import pyplot as plt

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
reset_outcomes(sum_outcomes,possible_sum_outcomes)

#set up plot
plt.rcParams.update({'font.size': 16})
plt.ion()
plt.show()
fig,ax = plt.subplots()
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
ax.set_xticks(possible_sum_outcomes)
ax.set_ylim(get_min(possible_sum_outcomes)-1,get_max(possible_sum_outcomes)+1);
#ax.set_ylabel("")
#ax.set_xlabel("")
bellcurve_xvals = possible_sum_outcomes
bellcurve, = ax.plot(bellcurve_xvals,bellcurve_xvals,color='grey', visible=False)
stepplot, = ax.step(sum_outcomes.keys(), sum_outcomes.values(), where='mid',color='blue')
stddevline1, = ax.plot([0,0],[0,0],color='red', visible=False)
stddevline2, = ax.plot([0,0],[0,0],color='red', visible=False)
meanline, = ax.plot([0,0],[0,0],color='lime', visible=False)
txt = ax.annotate("",xycoords='axes fraction', xy=(0.05,0.95), va='top', ha='left', fontsize='xx-large')

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
    
    global fig, ax, stepplot, txt, mean, meanline, bellcurve
    mean, stddev = calc_mean_and_stddev(sum_outcomes)
    #update annotation
    mean_0 = mean/outcomes_per_sum
    stddev_0 = 0 #stddev*math.sqrt(outcomes_per_sum)
    sum_oc_l = get_n_oc(sum_outcomes)
    txt.set_text("n=%d\n\nµ_%d=%.2f\nσ_%d=%.2f\nµ_1=%.2f\nσ_1=%.2f" % (sum_oc_l,outcomes_per_sum, mean, outcomes_per_sum, stddev, mean_0, stddev_0))
    
    #update plot
    sum_ocv = list(sum_outcomes.values())
    max_y = get_max(sum_ocv)+1
    ax.set_ylim(0,max_y);
    stepplot.set_ydata(sum_ocv)
    
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
