import Engine as en
import pygame as pg
import math
from Engine.audio import Sound
from Engine.textures import Animation
main = en.Engine((2**10, 768), 60, True)
MOUSE_SENSITIVITY = 1/200
MOVE_SPEED = .5
print("loading frames")
badframes = [pg.transform.scale(pg.image.load(f"Game/animations/badapple/frame{i}.png"),(256,256)).convert_alpha() for i in range(6572)]
print("frames loaded")
Badapple = Animation(badframes,30, main)
Appleaudio = Sound("Game/audio/badapple/apple.mp3",1)
def updatecam(cm : en.Camera, app : en.Engine):
    if app.inputcontroller.is_pressed(pg.K_z, False):
        cm.pos_x += math.cos(cm.angle) * app.get_dt/10 * MOVE_SPEED
        cm.pos_y += math.sin(cm.angle) * app.get_dt/10 * MOVE_SPEED
    if app.inputcontroller.is_pressed(pg.K_s, False):
        cm.pos_x -= math.cos(cm.angle) * app.get_dt/10 * MOVE_SPEED
        cm.pos_y -= math.sin(cm.angle) * app.get_dt/10 * MOVE_SPEED
    if app.inputcontroller.is_pressed(pg.K_q, False):
        cm.pos_x += math.sin(cm.angle) * app.get_dt/10 * MOVE_SPEED
        cm.pos_y -= math.cos(cm.angle) * app.get_dt/10 * MOVE_SPEED
    if app.inputcontroller.is_pressed(pg.K_d, False):
        cm.pos_x -= math.sin(cm.angle) * app.get_dt/10 * MOVE_SPEED
        cm.pos_y += math.cos(cm.angle) * app.get_dt/10 * MOVE_SPEED
    ls = app.inputcontroller.getevs
    if pg.MOUSEMOTION in ls:
        cm.angle += pg.mouse.get_rel()[0] * MOUSE_SENSITIVITY
Cam1 = en.Camera((10,30),main, lambda : None)
Cam1.updatefunc = lambda : updatecam(Cam1,main)
Cam2 = en.Camera((100,100),main, lambda : None)
Cam2.updatefunc = lambda : updatecam(Cam2,main)
def draw(app : en.Engine, pl):
    pg.draw.circle(app.display, "Red", app.normalisecoord(pl[0][0], pl[0][1]), app.normaliseradius(pl[1]))
LEVEL = [[0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,Badapple,Badapple,0,0,0,0],
         [0,0,0,0,Badapple,Badapple,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],]
en.Engine.setlevel(LEVEL)
main.run(lambda : None, lambda : None)
