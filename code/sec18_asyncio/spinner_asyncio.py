"""
    Des：python asyncio_18 asyncio_18 协程实现
    Date: 2021.05.17
"""

# asyncio_18 实现 spinner
import asyncio
import time
import sys
from itertools import cycle

@asyncio.coroutine
async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for c in cycle(r"|/-|\\"):
        status = c + ' ' + msg
        write(status)
        flush()
        write('\x08'*len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(" " * len(status) + "\x08" * len(status))


async def thinking():
    await asyncio.sleep(3)
    return 42

async def supervisor():

    spinner = asyncio.create_task(spin('thinking'))
    # spinner = asyncio_18(spinner('thinking'))
    print("spinner", spinner)
    result = await thinking()
    spinner.cancel()
    return result

if __name__ == '__main__':
    loop= asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print("Answer:", result)



