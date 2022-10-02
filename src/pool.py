
from queue import Queue
from threading import Thread
from typing import Any, Callable

class Worker(Thread):    
    def __init__(self, tasks: Queue):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, worker_count: int, max_tasks: int = 0):
        self.tasks = Queue(max_tasks)
        self.workers = [Worker(self.tasks) for _ in range(worker_count)]

    def add_task(self, func: Callable, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks.join()
