import aiohttp
import asyncio
from pprint import pprint

class ApiTester:
    def __init__(self,loader=None) -> None:
        self.loader=loader

    async def run_compilation(self,e):
        await asyncio.gather(self.get_data())

    async def get_data(self):
        temp_list =[]
        self.loader=False
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jsonplaceholder.typicode.com/posts') as response:
                res = await response.json()
                pprint(res)
        self.loader=True