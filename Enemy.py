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
        
        self._u = 0    #スプライト参照座標
        self._v = 0

        self._p = 0    #スプライト参照ページ

        self._vx = 0
        self._vy = 0

        self._show = True
        self.enable = True

        self._moveLR = 0

        self.sp = SPRITE()
        self.sp.spset(0, 16,16, 8,8, 0,32, 15)
    
    def SetPos(self, x, y):
        self._x = x
        self._y = y
    
    def SetShow(self, show:bool):
        self._show = show
        self.sp.spshow(show)
    
    def SpDef(self, page, w,h, ox, oy, u, v):

        self._p = page #参照ページ　

        self._w = w    #スプライトサイズ
        self._h = h
        
        self._u = u #参照座標
        self._v = v

        self.sp.spset(page, w,h ,ox,oy, u,v, 15)
    
    def Update(self):
        pass

    def Draw(self):
        pass

class Enemy01(ENEMY):

    def update(self):

        #self._x = 100
        #self._y = 100
        print("Enemy UpDate Call")

        if self._moveLR == 0:
            self._x += 8
            if Common.WIDTH < self._x:
                self._moveLR = 1
                self._y += 8
        elif self._moveLR == 1:
            self._x -= 8
            if 0 > self._x:
                self._moveLR = 0
                self._y += 8
        

        if Common.HEIGHT< self._y:
            self.enable = False
            
    def draw(self):
        print("Enemy Draw Call")

        if self._show:
            self.sp.spdraw(self._x, self._y)
        