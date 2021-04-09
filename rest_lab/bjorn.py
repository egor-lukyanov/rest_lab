import bjoern
from multiprocessing import Process
import signal

from wsgi import application

workers = []


def run(app):
    bjoern.listen(app, "0.0.0.0", port=8000, reuse_port=True)
    bjoern.run()


def kill_all(*args):
    for w in workers:
        w.terminate()


def start(num=8):
    for i in range(num):
        p = Process(name="worker-%d" % i, target=run, args=(application,))
        workers.append(p)
        p.start()


signal.signal(signal.SIGTERM, kill_all)
start()