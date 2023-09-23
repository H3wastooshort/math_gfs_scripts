from aiohttp import web
import numpy

new_data_flag=False
possible_outcomes = [1,2,3,4,5,6]
outcomes = {}
for o in possible_outcomes:
    outcomes[o] = 0

async def add_outcome(req):
    #add stuff
    new_data_flag=True
    return web.Response(text="ok")

#start webserver
app = web.Application()
app.add_routes([
    web.static('/', "./student"),
    web.post('/outcome', add_outcome)
])
web.run_app(app)

while True:
    
#https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
