import ast
import math
import time
import requests, json
import concurrent.futures
import asyncio, aiohttp

from fl_agg import model_aggregation
from main_server import send_agg_to_clients, reg_workers
from requests.exceptions import HTTPError
from datetime import datetime


# define rest end points here.
workers = reg_workers()

# Performs model training by calling /modeltrain endpoint at the workers
async def fetch(session, url):
    try:
        async with session.get(url + '/modeltrain') as response:
            return await response.text()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print('Other error occurred:', err)  # Python 3.6
    else:
        print('Success!')

# Loop executes the core functions. epoch keeps track of global iter and current_worker is a list used after 1st epoch,
# to keep track of which workers have completed tasks and ready for next round of training
async def sync(epoch, current_worker):
    g_tasks = []
    task_res =[]

    # For 1st epoch we wait untill all worker finishses their training, we keep track of epochs
    print('new_epoch:', epoch)
    if epoch == 1:
        print('current_worker:', current_worker)
        async with aiohttp.ClientSession() as session:
            for init_worker in workers:
                g_tasks.append(fetch(session, init_worker))
            done,pending = await asyncio.wait(g_tasks, return_when=asyncio.ALL_COMPLETED)

    else:
        print('current_worker:', current_worker)
        async with aiohttp.ClientSession() as session:
            for worker in current_worker:
                g_tasks.append(fetch(session, worker))
                # Once new training is launched, remove the workerid from current_worker list to avoid repeated training
                current_worker.remove(worker)
            done,pending = await asyncio.wait(g_tasks,return_when=asyncio.FIRST_COMPLETED)
            
    model_aggregation()

    # For workers that finished tasks, perform aggregation and send the new model. Add the workerid to current_worker
    # list for initiating next round of training
    for i in done:
        workerid = i.result()
        send_agg_to_clients(workerid)
        current_worker.append(workerid)
        print('Done worker:', current_worker)
        epoch = epoch + 1

async def main_sync():
    for i in range(1,50):
        epoch = i
        await sync(epoch, current_worker)

epoch = 0
current_worker = []
loop = asyncio.get_event_loop()
loop.run_until_complete(main_sync())
loop.run_forever()
