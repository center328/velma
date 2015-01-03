import zmq
import logging

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
pull_socket.bind('tcp://127.0.0.1:5000')
push_socket = context.socket(zmq.PUSH)
push_socket.bind('tcp://127.0.0.1:5001')

while True:
    try:
        task_data = pull_socket.recv_json()
        push_socket.send_json(task_data)
    except Exception, e:
        logging.error(e)

pull_socket.close()
push_socket.close()
context.term()
