import json

from rest_lab import utils

import cherrypy


class TestHandler:

    @cherrypy.expose
    def ping(self):
        return 'ok'

    @cherrypy.expose
    def simple(self):
        res = {"message": "OK"}
        return json.dumps(res)

    @cherrypy.expose
    def cpu(self):
        res = str(utils.fib())
        return res

    @cherrypy.expose
    def big(self):
        return utils.big_data()


if __name__ == '__main__':
    cherrypy.log.screen = False
    cherrypy.config.update({
                            'server.socket_port': 8000,
                            'server.socket_queue_size': 4000,
                            'server.numthreads': 300
                            })
    cherrypy.quickstart(TestHandler(), '/api', {
    })