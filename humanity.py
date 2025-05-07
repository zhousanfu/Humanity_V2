# https://testnet.humanity.org/api/rewards/balance
import os
import sys
import time
import json
import asyncio
import aiohttp




class Humanity:
    def __init__(self, token, proxie):
        self.base_url = 'https://testnet.humanity.org'
        self.proxie = proxie
        self.headers = {
                    'authorization': f'Bearer {token}',
                    'token': f'{token}',
                    'Accept': 'application/json, text/plain, */*',
                    'Origin': 'https://testnet.humanity.org',
                    'Referer': 'https://testnet.humanity.org/dashboard',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'Sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"'
                }
    
    async def get_balance(self):
        url = f'{self.base_url}/api/rewards/balance'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, proxy=self.proxie) as response:
                if response.status == 200:
                    response_json = await response.json()
                    print((f"humanity -ey***{token[-4:]}- response: {response_json}"))  

    async def post_check(self, retries=5):
        url = f'{self.base_url}/api/rewards/daily/check'

        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                async with session.post(url, headers=self.headers, proxy=self.proxie) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        if response_json['available']:
                            return True
                        break
                    elif response.status == 429:
                        wait_time = 10 ** attempt  # 指数退避
                        print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Request failed with status: {response.status}")
                        break
            return False

    async def post_claim(self, retries=5):
        url = f'{self.base_url}/api/rewards/daily/claim'

        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                async with session.post(url, headers=self.headers, proxy=self.proxie) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        print(response_json)
                        if response_json['available']:
                            return response_json
                        break
                    elif response.status == 429:
                        wait_time = 10 ** attempt  # 指数退避
                        print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"Request failed with status: {response.status}")
                        break
            return None

    async def run(self):
        check_v = await self.post_check()
        await asyncio.sleep(1)
        if check_v:
            await self.post_claim()
            await asyncio.sleep(1)
            await self.get_balance()
            await asyncio.sleep(1)


if __name__ == '__main__':
    while True:
        with open('token.txt', 'r') as f:
            tokens = [line.strip() for line in f]

        with open('proxy.txt', 'r') as f:
            proxies = [line.strip() for line in f]

        for index, token in enumerate(tokens):
            print(f"{index + 1}- start")
            h = Humanity(token, proxie=None)
            asyncio.run(h.run())
        
        # 等待24小时
        time.sleep(24 * 60 * 60)  # 24小时转换为秒
