import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

from wsgi import application


if __name__ == "__main__":
    container = tornado.wsgi.WSGIContainer(application)

    server = tornado.httpserver.HTTPServer(container)
    server.bind(8000)
    server.start(8)
    tornado.ioloop.IOLoop.current().start()