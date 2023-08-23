import pygame as pg

class Sound:
    _soundlists = []
    def __init__(self, snd, channel):
        self.sound = pg.mixer.Sound(snd)
        self.channel = pg.mixer.Channel(channel)
        Sound.addtolst(self)
    def play(self):
        if not self.channel.get_busy():
            self.channel.play(self.sound)
    @classmethod
    def addtolst(cls,it):
        cls._soundlists.append(it)
    @classmethod
    def getlst(cls):
        return cls._soundlists