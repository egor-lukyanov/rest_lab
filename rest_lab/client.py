import json
import os
import random
from time import sleep, time

import aiohttp
import asyncio

OTL = (
    'fieldsummary', 'command empty_check=isnotnull(phrase)', 'where currency="EUR"', 'convert ctime()',
    'eval currency_low=lower(currency)', 'filldown', 'rename dest as "destination country"', 'search index="linux-log"'
)

API = 'http://127.0.0.1:8000/api/'


class Measure:

    acc = 0
    ts = None
    tf = None
    calls = 0

    def __new__(cls, func):
        def wrapper(*args):
            cls.calls += 1
            start = time()
            res = func(*args)
            fin = time()
            cls.acc += fin - start
            return res
        return wrapper

    @classmethod
    def average(cls):
        return cls.calls // cls.acc

    @classmethod
    def real_world_average(cls):
        return cls.calls // (cls.tf - cls.ts)

    @classmethod
    def stats(cls):
        return f'Total time: {cls.acc}. Total requests: {cls.calls}. Avg {cls.average()} qps.'

    @classmethod
    def real_world_stats(cls):
        return f'Total time: {cls.tf - cls.ts}. Total requests: {cls.calls}. Avg {cls.real_world_average()} qps.'

    @classmethod
    def avg_response(cls):
        return f'Avg response time: {cls.acc / cls.calls}'


@Measure
async def get(client, url):
    try:
        async with client.get(url) as resp:

            json_resp = await resp.text()
            return json_resp
    except:
        print('error')
        pass


@Measure
async def post_json(client, url, data):
    try:
        async with client.post(url, json=data, headers={'content-type': 'application/json'}) as resp:
            json_resp = await resp.json()
            return json_resp
    except Exception as e:
        return e


@Measure
async def patch_json(client, url, data):
    try:
        async with client.patch(url, json=data, headers={'content-type': 'application/json'}) as resp:
            json_resp = await resp.json()
            return json_resp
    except Exception as e:
        return e


@Measure
async def delete(client, url):
    try:
        async with client.delete(url, headers={'content-type': 'application/json'}) as resp:
            json_resp = await resp.json()
            return json_resp
    except Exception as e:
        return e


def get_new_job_request():
    otl_req = '| '.join([random.choice(OTL) for _ in range(random.randrange(1, 10))])
    return {'request': otl_req}


async def job_loop():
    async with aiohttp.ClientSession() as client:

        # while True:
            devnull = open(os.devnull, 'w')

            job_data = await post_json(client, API + 'jobs/', get_new_job_request())
            job_url = job_data.get('url')

            job_data = await get(client, job_url)
            job_status = job_data.get('status')

            while not job_status == 'success':
                job_data = await get(client, job_url)
                job_status = job_data.get('status')

            result_data = await get(client, job_data.get('result'))
            payload = result_data.get('payload')
            devnull.write(payload[0])

            print(job_data.get('result'))

            await patch_json(client, job_url, {'completed': True})

            devnull.close()


async def request(endpoint):
    print('Sending req', endpoint)
    async with aiohttp.ClientSession() as client:
        data = await get(client, API + endpoint)
    print('Got', endpoint)



async def main():
    Measure.ts = time()
    for _ in range(10):
        coros = asyncio.gather(
            *[
                * [request('big') for _ in range(20)],
                * [request('cpu') for _ in range(20)],
                * [request('simple') for _ in range(1960)],

            ]
        )
        await coros
    Measure.tf = time()
    print(Measure.stats())
    print(Measure.real_world_stats())

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

