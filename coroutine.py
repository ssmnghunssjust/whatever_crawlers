# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     coroutine.py 
   Description :   None
   Author :        LSQ
   date：          2020/8/16
-------------------------------------------------
   Change Activity:
                   2020/8/16: None
-------------------------------------------------
"""
import asyncio
import threading
import time
from aiomultiprocess import Pool

async def hello():
    print('hello world!  %s'%threading.current_thread())

    # yield from asyncio.sleep(5)
    await asyncio.sleep(5)
    print('hello again!  %s'%threading.current_thread())

loop = asyncio.get_event_loop()
# task1 = loop.create_task(hello)
# task2 = loop.create_task(hello)
task = [ asyncio.ensure_future(hello()) for _ in range(3)]
t1 = time.time()
# loop.run_until_complete(asyncio.gather(task1,task2))
loop.run_until_complete(asyncio.wait(task))
loop.close()
t2 = time.time()
print('time:%s'%(t2-t1))