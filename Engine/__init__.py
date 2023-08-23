"""
manages the Game instance with all the settings
"""
import pygame as pg
from . import controllers as ctl
from .camera import Camera
from .textures import Animation
from .audio import Sound
pg.init()
class Engine:
    _CurrentLevel = []
    def __init__(self, res, fps, debug = False):
        self.display = pg.display.set_mode(res, pg.RESIZABLE)
        self.inputcontroller = ctl.InputController()
        self.timecontroller = ctl.TimeController(fps)
        self._debugmode = debug
        self.res = res
        self._cameraindex = 0
        self.coef_hor, self.coef_vert = 1,1
    def _updateins(self):
        """
        inside updates
        """
        self.inputcontroller.update()
        self.timecontroller.update()
        for animation in Animation.getlst():
            animation.update()
        for music in Sound.getlst():
            music.play()

    def run(self,updatefunc, drawfunc):
        """
        runs the window and uses two funcs to manipulate the game
        """
        self.timecontroller.start()
        while not self.inputcontroller.quitevent:
            self.display.fill("black")
            self._updateins()
            updatefunc()
            drawfunc()

            if self._debugmode:
                pg.display.set_caption(str(self.timecontroller))
            self.coef_hor,self.coef_vert = self.display.get_width()/self.res[0], self.display.get_height()/self.res[1]
            for camera in Camera.getin():
                if camera == camera.getin()[self._cameraindex]:
                    camera.updatefunc()
                    camera.raycast()

                camera.draw()
            if self.inputcontroller.is_pressed(pg.K_TAB, True):
                self.nextcam()
            for coord in self.level_coord:
                pg.draw.rect(self.display,"white",(*self.normalisecoord(coord[0] * 10, coord[1] * 10), *self.normalisescale(10, 10)), 1)
            pg.display.flip()

    def nextcam(self):
        self._cameraindex += 1
        self._cameraindex %= len(Camera.getin())
    def normalisecoord(self,pos_x,pos_y):
        return pos_x * self.coef_hor, pos_y * self.coef_vert

    def normalisescale(self,scale_x,scale_y):
        return scale_x * self.coef_hor, scale_y * self.coef_vert

    def normaliseradius(self,rad):
        return rad * (self.coef_hor + self.coef_vert)/2
    @property
    def get_dt(self):
        return self.timecontroller.get_dt
    @property
    def is_debug(self):
        return self._debugmode

    @classmethod
    def setlevel(cls,lev : list):
        if not isinstance(lev,list):
            raise TypeError("level is not supported as it is not a list")
        cls._CurrentLevel = lev

    @classmethod
    def get_texture(cls,txt):
        return cls._CurrentLevel
    @property
    def getlevel(self):
        return Engine.currentlevel()
    @classmethod
    def currentlevel(cls):
        return cls._CurrentLevel

    @property
    def level_coord(self):
        coordinates = []
        lev = self.getlevel
        for igrekis in range(len(lev)):
            for ekis in range(len(lev[igrekis])):
                if lev[igrekis][ekis]:
                    coordinates.append((ekis,igrekis))
        return coordinates