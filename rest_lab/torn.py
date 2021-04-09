from tornado import gen
from tornado.web import RequestHandler, Application
import tornado.httpserver
import tornado.ioloop

import utils


class PingHandler(RequestHandler):
    URI = r'/api/ping'

    async def get(self):
        self.write('ok')
        await self.flush()


class SimpleHandler(RequestHandler):
    URI = r'/api/simple'

    async def get(self):
        self.set_header('Content-type', 'application/json')
        self.write(utils.simple())
        await self.flush()


class CPUHandler(RequestHandler):
    URI = r'/api/cpu'

    async def get(self):
        res = str(utils.fib())
        self.set_header('Content-type', 'text/plain')
        self.write(res)
        await self.flush()


class BigHandler(RequestHandler):
    URI = r'/api/big'

    async def get(self):
        self.set_header('Content-type', 'text/event-stream')
        data = utils.big_data()

        for chunk in data:
            self.write(chunk)
            await self.flush()
            await gen.sleep(0.00001)


if __name__ == "__main__":
    handlers = (PingHandler, SimpleHandler, CPUHandler, BigHandler)
    app = Application(
        [(handler.URI, handler) for handler in handlers]
    )

    server = tornado.httpserver.HTTPServer(app)
    server.bind(8000)
    server.start(8)
    tornado.ioloop.IOLoop.current().start()