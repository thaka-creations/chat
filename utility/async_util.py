import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/ws/chat/test/') as resp:
            print(resp.status)
            print(await resp.text())


def process_async():
    asyncio.run(main())
