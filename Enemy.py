# python 3 Program

from Sprite import SPRITE
import pyxel
import Sprite
import Common

class ENEMY:
    def __init__(self):

        self._x = -100      #スプライト表示座標
        self._y = -100
        self._w = 16    #スプライトサイズ
        self._h = 16
        self.enable = True
        self._vx = 0
        self._vy = 0
        self._show = False

        self.move = 0

        self.sp = SPRITE()
        self.sp.spset(0,16,16, 8,8, 0,32, 15)
    
    def SetPos(self, x, y):
        self._x = x
        self._y = y
    
    def SetShow(self, show:bool):
        self._show = show
        self.sp.spshow(show)
    
    def SpDef(self, u,v, w,h):
        self._w = w    #スプライトサイズ
        self._h = h

        self.sp.spset(0, 16,16, 8,8, 0,32, 15)# .spset(0, w,h, 8,8, u,v, 15)
    
    def Update(self):
        pass

    def Draw(self):
        pass

class Enemy01(ENEMY):

    def update(self):

        self._x = 100
        self._y = 100
        print("Enemy UpDate Call")
        return

        if self.move ==0:
            self._x += 1
            if Common.WIDTH < self._x:
                self.move = 1
        elif self.move == 1:
            self._x -= 1
            if 0 > self._x:
                self.move = 0
        
        self._y += 5

        if Common.HEIGHT< self._y:
            self.enable = False
            
    def draw(self):
        print("Enemy Draw Call")

        if self._show:
            self.sp.spdraw(self._x, self._y)
        