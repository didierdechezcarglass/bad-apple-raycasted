"""
controls the camera for raycasting purposes
all credits to coderspace for the raycast() function and get_render() function
"""
import pygame as pg
import math
class Camera:
    """
    writes data to the game
    """
    _instances = []
    def __init__(self, coords, app, updatefunc = lambda : None):
        self.angle = 0
        self.app = app
        self.pos_x, self.pos_y = coords
        self._fov = math.pi/3
        self.ray_res = []
        self.updatefunc = updatefunc
        Camera.addtolist(self)
    def get_render(self, num_rays):
        TEXTURE_SIZE = 256
        scale = (self.app.display.get_width()) // num_rays
        HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
        for ray, values in self.ray_res:
            depth, proj_height, texture, offset = values
            col = texture.image.subsurface( offset * (TEXTURE_SIZE - scale),0,scale,TEXTURE_SIZE)
            col = pg.transform.scale(col, (scale, proj_height))
            wall_pos = (ray * scale, self.app.display.get_height() //2 - proj_height // 2)
            self.app.display.blit(col,wall_pos)
    def raycast(self):
        """
        raycast with a step of 10 for each rays (max depth will be defined to 8 jumps or more
        this doesn't floorcast
        """
        self.ray_res = []
        num_rays = (self.app.display.get_width() // 2)
        #position on the "game map"
        MAPX,MAPY = self.pos_x // 10, self.pos_y // 10
        #x and y in float
        ORIGINX,ORIGINY = self.pos_x / 10 , self.pos_y / 10
        HALFFOV = self._fov/2
        start_angle = self.angle - HALFFOV + .000001
        MAX_JUMPS = 30
        LEVEL = self.app.level_coord
        delta = self._fov/num_rays
        screen_dist = (self.app.display.get_width() // 2) / (math.tan(HALFFOV))


        for ray in range(num_rays):
            cos_a = math.cos(start_angle)
            sin_a = math.sin(start_angle)
            tx_vert, tx_hor = 0,0
            #vertical configuration
            pos_xv, delta_xv = (MAPX + 1, 1) if cos_a > 0 else (MAPX -.00001, -1)
            # delta_h = dx/cos_a (trigonometry + triangle)
            delta_hv = delta_xv/cos_a
            delta_yv = delta_hv * sin_a
            depth_vert = (pos_xv - ORIGINX) / cos_a
            pos_yv = ORIGINY + depth_vert * sin_a

            for _ in range(MAX_JUMPS):
                pos = int(pos_xv),int(pos_yv)
                if pos in LEVEL:
                    tx_hor = self.app.getlevel[int(pos_yv)][int(pos_xv)]
                    break
                pos_xv += delta_xv
                pos_yv += delta_yv
                depth_vert += delta_hv

            #horizontal configuration
            #what i understand
            pos_yh, delta_yh = (MAPY + 1, 1) if sin_a > 0 else (MAPY - .00001, -1)
            #same reasoning with the triangle used before, needs to be desmosed to visualize it more clearly
            delta_hh = delta_yh / sin_a
            # DY IS NOT ALWAYS 1
            delta_xh = delta_hh * cos_a

            # what still need to be understood

            depth_hor = (pos_yh - ORIGINY) / sin_a
            pos_xh = ORIGINX + depth_hor * cos_a
            for _ in range(MAX_JUMPS):
                pos = int(pos_xh), int(pos_yh)
                if pos in LEVEL:
                    tx_vert = self.app.getlevel[int(pos_yh)][int(pos_xh)]
                    break
                pos_xh += delta_xh
                pos_yh += delta_yh
                depth_hor += delta_hh
            if depth_vert < depth_hor:
                depth, tx = depth_vert, tx_vert
                pos_yv %= 1
                ofs = pos_yv if cos_a > 0 else (1 - pos_yv)
            else:
                depth, tx = depth_hor, tx_hor
                pos_xh %= 1
                ofs = (1 - pos_xh) if sin_a > 0 else pos_xh
            if tx == 0 and tx_hor != 0:
                tx = tx_hor
            if tx == 0 and tx_vert != 0:
                tx = tx_vert
            # prevents fisheye effect
            depth *= math.cos(self.angle - start_angle)
            proj_height = screen_dist / (depth + 0.0001)
            if tx:
                self.ray_res.append((ray,(depth, proj_height, tx, ofs)))
            #pg.draw.line(self.app.display,"yellow",self.app.normalisecoord(10*ORIGINX,10*ORIGINY),self.app.normalisecoord(10*(ORIGINX  + depth * cos_a),10*(ORIGINY + depth * sin_a)))
            scale = (self.app.display.get_width()) // num_rays
            pg.draw.rect(self.app.display,"white", (ray * scale, self.app.display.get_height()//2 - proj_height // 2,scale, proj_height))
            start_angle += delta
        self.get_render(num_rays)
        #pg.draw.line(self.app.display,"green",self.app.normalisecoord(self.pos_x,self.pos_y),self.app.normalisecoord(self.pos_x + 10*math.cos(self.angle- HALFFOV),self.pos_y + 10*math.sin(self.angle - HALFFOV)))
        #pg.draw.line(self.app.display, "green", self.app.normalisecoord(self.pos_x, self.pos_y),
        #             self.app.normalisecoord(self.pos_x + 10 * math.cos(self.angle + HALFFOV), self.pos_y + 10 * math.sin(self.angle + HALFFOV)))
        #pg.draw.circle(self.app.display,"red",self.app.normalisecoord(10*MAPX,10*MAPY),self.app.normaliseradius(1))






    def setfov(self, fov):
        self._fov = fov
    def draw(self):
        if self.app.is_debug:
            pg.draw.circle(self.app.display,"green",self.app.normalisecoord(self.pos_x,self.pos_y), self.app.normaliseradius(2))
            pg.draw.line(self.app.display,"yellow", self.app.normalisecoord(self.pos_x,self.pos_y), self.app.normalisecoord(self.pos_x + 10*math.cos(self.angle),self.pos_y + 10*math.sin(self.angle)))
    @classmethod
    def addtolist(cls,it):
        cls._instances.append(it)

    @classmethod
    def getin(cls):
        return cls._instances
