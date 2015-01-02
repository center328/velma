import logging
import os
import uuid

from tornado.ioloop import IOLoop
import tornado.web
import tornado.websocket


global_clients = {}
rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class StreamWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        global_clients[self.id] = self
        self.write_message('connected')
        logging.info(
            'WebSocket connection opened from %s', self.request.remote_ip)

    def on_message(self, message):
        logging.info(
            'Received message from %s: %s', self.request.remote_ip, message)

    def on_close(self):
        logging.info('WebSocket connection closed.')
        del global_clients[self.id]


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
