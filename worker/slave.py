import logging

import zmq
import tasks

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
pull_socket.connect('tcp://127.0.0.1:5001')
pub_socket = context.socket(zmq.PUB)
pub_socket.bind('tcp://127.0.0.1:5002')

while True:
    try:
        task_data = pull_socket.recv_json()
        task = task_data.pop('task')
        ws_id = task_data.pop('ws_id')
        task_kwargs = task_data.pop('task_kwargs')
        result = getattr(tasks, task)(**task_kwargs)
        print "task done!"
        print result
        pub_socket.send_json({'result': result, 'ws_id': ws_id})
    except Exception, e:
        logging.error(e)

pull_socket.close()
pub_socket.close()
context.term()
