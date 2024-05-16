import queue

import aiohttp
import asyncio
from queue import Queue


async def process_(session, data: dict):
    if data['method'] == 'GET':
        async with session.get(url=data['url'], params=data['payload'], ssl=False) as resp:
            return await resp.json()
    else:
        async with session.post(url=data['url'], json=data['payload'], ssl=False) as resp:
            return await resp.json()


async def main(que: Queue):
    tasks = []
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                item = que.get_nowait()
                tasks.append(asyncio.ensure_future(process_(session, item)))
            except queue.Empty:
                break

        results_ = await asyncio.gather(*tasks)
        return results_


def process_async(que: Queue):
    res = asyncio.run(main(que))
    return res
