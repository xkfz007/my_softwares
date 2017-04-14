import time
import zmq
import uuid
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Manager

# TODO: handle failed tasks

_GLOBAL_PRINT_LOCK = Lock()
_TASK_PORT = 5000
_RESULT_PORT = 5001
_WORKER_ACK_PORT = 9000
_CONTEXT = zmq.Context()
_PROCESSES = []  # All workers and sinker process
_TASK_OUT = None  # PUSH socket for dispatching _TASKS to workers
_TASKS = None  # All [download] _TASKS. Instance of multiprocessing.Manager.dict()


class Task(object):
    def __init__(self, task_id, command, status='start'):
        '''
        @param task_id Unique id for a task
        @param command An object
        '''
        self.id = task_id
        self.command = command
        self.status = status

    def set_done(self):
        self.status = 'done'

    def is_done(self):
        return 'done' == self.status

    def __repr__(self):
        return 'task {id}: stauts {status}'.format(id=self.id, status=self.status)


def blocking_print(message):
    _GLOBAL_PRINT_LOCK.acquire()
    print(message)
    _GLOBAL_PRINT_LOCK.release()


def _worker(action):
    worker_id = uuid.uuid4()
    blocking_print('create worker [{id}]'.format(id=worker_id))

    try:
        task_in = _CONTEXT.socket(zmq.PULL)
        task_in.connect('tcp://localhost:{port}'.format(port=_TASK_PORT))

        result_out = _CONTEXT.socket(zmq.REQ)
        result_out.connect('tcp://localhost:{port}'.format(port=_RESULT_PORT))

        # sync worker to client
        worker_ack_out = _CONTEXT.socket(zmq.REQ)
        worker_ack_out.connect('tcp://localhost:{port}'.format(port=_WORKER_ACK_PORT))
        worker_ack_out.send(b'')
        blocking_print('waiting to start worker [{id}]'.format(id=worker_id))
        worker_ack_out.recv()  # blocking wait client to response, then start working process
        blocking_print('worker [{id}] stats'.format(id=worker_id))

        # main working loop
        while True:
            blocking_print('worker [{id}] is waiting for task'.format(id=worker_id))
            task_msg = task_in.recv_json()
            blocking_print('receive task_msg: {msg}'.format(msg=task_msg))
            task = Task(task_msg['id'], task_msg['command'])
            blocking_print('worker [{id}] is working on {task}'.format(id=worker_id, task=task.id))

            if action(task):
                task.set_done()

            result_out.send_json(task.__dict__)

            blocking_print('worker [{id}] is sending out result'.format(id=worker_id))
            result_out.recv()
    except Exception as e:
        blocking_print('worker [{id}] Error: {error}'.format(id=worker_id, error=e.strerror))


def _sink(_TASKS):
    sink_id = uuid.uuid4()
    blocking_print('create sink [{id}]'.format(id=sink_id))

    try:
        result_in = _CONTEXT.socket(zmq.REP)
        result_in.bind('tcp://*:{port}'.format(port=_RESULT_PORT))

        while True:
            task_msg = result_in.recv_json()
            task = Task(task_msg['id'], task_msg['command'], task_msg['status'])
            blocking_print('sink [{id}] received result of task {task_id}'.format(id=sink_id, task_id=task.id))
            _TASKS[task.id] = task
            # print(_TASKS)
            result_in.send(b'')
    except Exception as e:
        blocking_print('sink [{id}] Error: {error}'.format(id=sink_id, error=e.strerror))


def start(task_processor, num_workers=4):
    global _PROCESSES
    global _TASKS
    manager = Manager()
    _TASKS = manager.dict()

    # create sink
    p = Process(target=_sink, args=(_TASKS, ))
    _PROCESSES.append(p)
    p.start()

    # create workers
    for i in range(num_workers):
        p = Process(target=_worker, args=(task_processor,))
        _PROCESSES.append(p)
        p.start()

    try:
        # synchronise active workers
        ack_in = _CONTEXT.socket(zmq.REP)
        ack_in.bind('tcp://*:{port}'.format(port=_WORKER_ACK_PORT))
        num_active_workers = 0
        while num_active_workers < num_workers:
            ack_in.recv()
            ack_in.send(b'')
            num_active_workers += 1

        # create _TASK_OUT socket
        global _TASK_OUT
        _TASK_OUT = _CONTEXT.socket(zmq.PUSH)
        _TASK_OUT.bind('tcp://*:{port}'.format(port=_TASK_PORT))
    except Exception as e:
        print('Error in start worker {error}'.format(error=e.strerror))
        stop()


def stop():
    for p in _PROCESSES:
        print('stop process [{pid}]'.format(pid=p.pid))
        p.terminate()


def dedicate(task):
    '''
    @param task Task object
    '''
    if not _TASK_OUT:
        blocking_print('Error _TASK_OUT is None. start() the downloader')
        return

    if task.id in _TASKS:
            blocking_print('task: {task_id} is processed'.format(task_id=task.id))
    else:
        _TASKS[task.id] = task
        blocking_print('send task: {task}'.format(task=task.id))
        _TASK_OUT.send_json(task.__dict__)


def have_all__TASKS_done():
    all__TASKS_done = True
    for k, v, in _TASKS.items():
        if not v.is_done():
            all__TASKS_done = False
            break
    return all__TASKS_done


def print_all_tasks():
    print(_TASKS)


def main():
    def simple_action(task):
        '''
        @param task Task instance
        @return True indicating task done, False otherwise
        '''
        blocking_print('procesing task: {id}'.format(id=task.id))
        import random
        time.sleep(random.randint(1, 10))
        return True

    # start boss (including worker and sinker processes)
    start(num_workers=4, task_processor=simple_action)

    # dispatch dummy tasks
    for i in range(50):
        import random
        task_id = random.randint(1, 30)
        task = Task(task_id, {})
        dedicate(task)
        time.sleep(0.5)

    # check all tasks done before stop boss
    total_check = 0
    while not have_all__TASKS_done():
        blocking_print('Waiting for all _TASKS done')
        time.sleep(1)
        total_check += 1
        if total_check > 50:
            break

    # stop boss (including worker and sinker processes)
    stop()
    print_all_tasks()


if __name__ == '__main__':
    main()
