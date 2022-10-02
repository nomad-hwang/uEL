
from queue import Queue
from threading import Thread
import time
from typing import Any, Callable

from pool import ThreadPool

class EventCallback:
    def __init__(self, callbacks: set = set()):
        self._callbacks = callbacks

    def subscribe(self, callback: Callable):
        self._callbacks.add(callback)

    def unsubscribe(self, callback: Callable):
        self._callbacks.remove(callback)

    def __iter__(self):
        return iter(self._callbacks)

    def __repr__(self):
        return f"EventCallback({self._callbacks!r})"

class Event(EventCallback):
    def __init__(self, name: str = None, data: Any = None, loop: "EventLoop" = None):
        super().__init__()
        self._name = name
        self._data = data

        if loop is None:
            loop = get_event_loop()
        self._loop = loop

    def emit(self, data: Any = None):
        self._data = data
        self._loop.add_event(self)

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return f"Event({self._name!r}, {self._data!r})"

class EventLoop(Thread):
    def __init__(self, worker_count: int = 5):
        super().__init__()
        self.daemon = True        
        self._queue = Queue()
        self._pool = ThreadPool(worker_count)
        self.start()

    def add_event(self, event: Event):
        self._queue.put_nowait(event)

    def run(self):
        while True:
            event = self._queue.get()
            for callback in event:
                self._pool.add_task(callback, event)
            self._queue.task_done()


event_loop = EventLoop()

def get_event_loop() -> EventLoop:
    return event_loop

def emit(event: Event, data: Any = None):
    event.emit(data)

def subscribe(event: Event, callback: Callable):
    event.subscribe(callback)

def unsubscribe(event: Event, callback: Callable):
    event.unsubscribe(callback)


if __name__ == '__main__':
    event = Event('test event')
    emit(event, {'test': 'test'})
    subscribe(event, lambda e: print(e))
    
    time.sleep(1)