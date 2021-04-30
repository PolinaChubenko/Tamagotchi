from numbers import Number
from typing import Callable
import threading
import pygame


class AlreadyRunning(Exception):
    pass


class IntervalNotValid(Exception):
    pass


class SetInterval:
    def __init__(self, func: Callable = None, sec: Number = None, args=None, autostart=True):
        if args is None:
            args = []
        self.running = False
        self.func = func
        self.interval = sec
        self.f_return = None
        self.args = args
        self.run_once = None
        self.run_once_args = None

        if (func is not None) and (sec is not None) and autostart:
            self.running = True
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()

    def start(self):
        if not self.running:
            self.running = True
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()
        else:
            raise AlreadyRunning("Tried to run an already run interval")

    def stop(self):
        self.running = False

    def loop(self):
        if self.running:
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()
            function_, args_ = self.func, self.args

            if self.run_once is not None:
                run_once, self.run_once = self.run_once, None
                result = run_once(*self.run_once_args)
                self.run_once_args = None

                if result is False:
                    return  # cancel the interval right now

            self.f_return = function_(*args_)

    def change_interval(self, sec: Number):
        if self.running:
            self.TIMER.cancel()

        self.interval = sec

        if self.running:
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()

    def change_next_interval(self, sec: Number):
        self.interval = sec

    def change_func(self, func: Callable, args=None):
        if args is None:
            args = []

        self.func = func

        if args is not None:
            self.args = args

    def change_argument(self, new_argument=None):
        if new_argument is None:
            new_argument = []
        self.args = new_argument

    def run_func_once(self, func: Callable, args=None):
        if args is None:
            args = []
        self.run_once = func
        self.run_once_args = args

    def get_return(self):
        return self.f_return


def set_timer(event_obj, interval, autostart=True):
    return SetInterval(func=lambda x: pygame.event.post(x), sec=interval, args=[event_obj], autostart=autostart)
