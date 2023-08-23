"""
Animations of items in pygame
"""
import pygame as pg
from math import floor

class Animation:
    """
    animated object with set number of fps
    """
    _animlist = []
    def __init__(self, imgs, fps, app):
        """
        constructor
        """
        self.frames = imgs
        self.index = 0
        self.delta_index = 0
        self.app = app
        self.fps = fps
        Animation.addtolist(self)
    def update(self):
        """
        modifies the index of the image
        """
        self.delta_index += self.fps/1000 * self.app.get_dt
        self.index = floor((self.index + self.delta_index) % len(self.frames))
        #reset the delta_index once it reaches one so that the floor function resets
        self.delta_index %= 1

    @property
    def image(self):
        """
        returns current image
        """
        return self.frames[self.index]

    @classmethod
    def addtolist(cls,it):
        """
        adds to class list to grab parameter it in the game
        """
        cls._animlist.append(it)

    @classmethod
    def getlst(cls):
        """
        gives the animation list for the game
        """
        return cls._animlist

