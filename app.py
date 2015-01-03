import json
import logging
import os
import uuid

from tornado.ioloop import IOLoop
import tornado.web
import tornado.websocket

import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

ioloop.install()

ctx = zmq.Context()
task_socket = ctx.socket(zmq.PUSH)
task_socket.connect('tcp://127.0.0.1:5000')

logging.getLogger().setLevel(logging.INFO)

global_clients = {}
rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))


class ZMQPubSub(object):

    def __init__(self, callback):
        self.callback = callback

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://127.0.0.1:5002')
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.callback)

    def subscribe(self):
        self.socket.setsockopt(zmq.SUBSCRIBE, '')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class StreamWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = str(uuid.uuid4())
        global_clients[self.id] = self
        self.pubsub = ZMQPubSub(self.on_data)
        self.pubsub.connect()
        self.pubsub.subscribe()
        self.write_message('connected')
        logging.info(
            'WebSocket connection opened from %s', self.request.remote_ip)

    def on_message(self, message):
        logging.info(
            'Received message from %s: %s', self.request.remote_ip, message)
        task_kwargs = {'query': str(message)}
        task_socket.send_json({
            'task': 'get_summary',
            'task_kwargs': task_kwargs,
            'ws_id': self.id
        })

    def on_close(self):
        logging.info('WebSocket connection closed.')
        del global_clients[self.id]

    def on_data(self, data):
        for result in data:
            result_dict = json.loads(result)
            ws_id = result_dict['ws_id']
            res = json.dumps(result_dict["result"])
            print global_clients
            global_clients[ws_id].write_message(res)


def main():
    settings = dict(
        template_path=rel('templates'),
        static_path=rel('static'),
        debug=True
    )

    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/ws', StreamWebSocketHandler)
    ], **settings)

    application.listen(address='127.0.0.1', port=8080)
    logging.info("Started listening at 127.0.0.1:8080.")
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
