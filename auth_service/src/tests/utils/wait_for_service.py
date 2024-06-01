import aiohttp
import asyncio
import time


async def get_status(service_url, client):
    raw_response = await client.get(service_url)
    return raw_response.status


async def wait_for_ok(service_url):
    async with aiohttp.ClientSession() as client:
        for _ in range(100):
            time.sleep(10)
            status = await get_status(service_url, client)
            if status == 200:
                break


service_url = "http://service:8000/api/v1/films/"
loop = asyncio.new_event_loop()
loop.run_until_complete(wait_for_ok(service_url))
