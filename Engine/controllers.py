"""
manages mouse and keyboard inputs
"""
import pygame as pg

class InputController:
    def __init__(self):
        self._mouse = pg.mouse.get_pressed(num_buttons=5)
        self._keys = pg.key.get_pressed()
        self.quitevent = False
        self._onemouse = [False] * 5
        self._onekeys = []
        self._listevs = []


    def update(self):
        self._listevs = []
        self._keys = pg.key.get_pressed()
        self._mouse = pg.mouse.get_pressed(num_buttons=5)
        self._onekeys = []
        self._onemouse = [False] *  5
        for event in pg.event.get():
            listev = True
            if event.type == pg.QUIT:
                listev = False
                self.quitevent = True
            if event.type == pg.MOUSEBUTTONDOWN:
                listev = False
                self._onemouse[event.button - 1] = True
            if event.type == pg.KEYDOWN:
                listev = False
                self._onekeys.append(event.key)
            if listev:
                self._listevs.append(event.type)
    @property
    def getevs(self):
        return self._listevs
    def is_pressed(self,key, once : bool):
        return key in self._onekeys if once else self._keys[key]

    def is_clicked(self, btn, once : bool):
        return self._onemouse[btn - 1]  if once else self._mouse[btn - 1]
    @property
    def getkeys(self):
        return self._onekeys
    @property
    def getmouse(self):
        return self._onemouse

    def __str__(self):
        return "InputController is working"

class TimeController:
    """
    controls time, delta time, and execution time
    """
    def __init__(self, fps):
        self._clock = None
        self._delta_time = 0
        self._exectime = 0
        self.fps = fps
    def start(self):
        self._clock = pg.time.Clock()
    def update(self):
        self._delta_time = self._clock.tick(self.fps)
        self._exectime += self._delta_time
    @property
    def get_dt(self):
        return self._delta_time
    @property
    def get_time(self):
        return self._exectime
    def __str__(self):
        return f"{self._delta_time}, {self._clock.get_fps():.2f}, {self._exectime//1000}"
