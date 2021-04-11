import threading
import pygame
from numbers import Number


class AlreadyRunning(Exception):
    pass


class IntervalNotValid(Exception):
    pass


class SetInterval:
    def __init__(self, func=None, sec=None, args=None, autostart=True):
        if args is None:
            args = []
        self.running = False
        self.func = func
        self.interval = sec
        self.Return = None
        self.args = args
        self.run_once = None
        self.run_once_args = None

        if (func is not None) and (sec is not None) and autostart:
            self.running = True

            if not callable(func):
                raise TypeError("non-callable object is given")

            if not isinstance(sec, Number):
                raise TypeError("A non-numeric object is given")

            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()

    def start(self):
        if not self.running:
            if not self.is_valid():
                raise IntervalNotValid("The function and/or the " +
                                       "interval hasn't provided or invalid.")
            self.running = True
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()
        else:
            raise AlreadyRunning("Tried to run an already run interval")

    def stop(self):
        self.running = False

    def is_valid(self):
        if not callable(self.func):
            return False

        if not isinstance(self.interval, Number):
            return False
        return True

    def loop(self):
        if self.running:
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()
            function_, args_ = self.func, self.args

            if self.run_once is not None:  # someone has provide the run_once
                run_once, self.run_once = self.run_once, None
                result = run_once(*self.run_once_args)
                self.run_once_args = None

                # if and only if the result is False. not accept "None"
                # nor zero.
                if result is False:
                    return  # cancel the interval right now

            self.Return = function_(*args_)

    def change_interval(self, sec):

        if not isinstance(sec, Number):
            raise TypeError("A non-numeric object is given")

        # prevent error when providing interval to a blueprint
        if self.running:
            self.TIMER.cancel()

        self.interval = sec

        # prevent error when providing interval to a blueprint
        # if the function hasn't provided yet
        if self.running:
            self.TIMER = threading.Timer(self.interval, self.loop)
            self.TIMER.start()

    def change_next_interval(self, sec):
        if not isinstance(sec, Number):
            raise TypeError("A non-numeric object is given")

        self.interval = sec

    def change_func(self, func, args=None):
        if args is None:
            args = []
        if not callable(func):
            raise TypeError("non-callable object is given")

        self.func = func

        if args is not None:
            self.args = args

    def change_argument(self, new_argument=None):
        if new_argument is None:
            new_argument = []
        self.args = new_argument

    def run_once(self, func, args=None):
        if args is None:
            args = []
        self.run_once = func
        self.run_once_args = args

    def get_return(self):
        return self.Return


def set_timer(event_obj, interval, autostart=True):
    return SetInterval(func=lambda x: pygame.event.post(x), sec=interval, args=[event_obj], autostart=autostart)
