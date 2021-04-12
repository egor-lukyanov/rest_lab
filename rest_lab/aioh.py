import asyncio
import json
import socket
import traceback
from concurrent.futures import ProcessPoolExecutor

from aiohttp import web

import utils


async def simple(request):
    res = {"message": "OK"}
    return web.Response(text=json.dumps(res))


async def ping(request):
    return web.Response(text='ok')


async def bigdata(request):
    resp = web.StreamResponse(headers={"Content-Type": "text/event-stream"})
    resp.enable_chunked_encoding()
    await resp.prepare(request)
    data = utils.big_data()

    for chunk in data:
        await resp.write(chunk)
        await asyncio.sleep(0.00001)

    await resp.write_eof()
    return resp


async def cpubounded(_):
    res = str(utils.fib())
    return web.Response(text=res)


def mk_socket(host="127.0.0.1", port=8000, reuseport=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if reuseport:
        SO_REUSEPORT = 15
        sock.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)
    sock.bind((host, port))
    return sock


async def start_server():
    try:
        host = "127.0.0.1"
        port = 8000
        reuseport = True
        app = web.Application()

        app.add_routes(
            [
                web.get('/api/simple', simple),
                web.get('/api/big', bigdata),
                web.get('/api/cpu', cpubounded),
                web.get('/api/ping', ping),

            ]
        )
        runner = web.AppRunner(app)
        await runner.setup()
        sock = mk_socket(host, port, reuseport=reuseport)
        srv = web.SockSite(runner, sock)
        await srv.start()
        print('Server started')
        return srv, app, runner
    except Exception:
        traceback.print_exc()
        raise


async def finalize(srv, app, runner):
    sock = srv.sockets[0]
    app.loop.remove_reader(sock.fileno())
    sock.close()

    await runner.cleanup()
    srv.close()
    await srv.wait_closed()
    await app.finish()


def init():
    loop = asyncio.get_event_loop()
    srv, app, runner = loop.run_until_complete(start_server())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete((finalize(srv, app, runner)))


if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        for i in range(8):
            executor.submit(init)
