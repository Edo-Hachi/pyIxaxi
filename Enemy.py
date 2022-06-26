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

        self._vx = 0    #ベクトル移動速度
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

#Enemy Type Move Left2Right
class Enemy01(ENEMY):
    STAT_DOWN = 0
    STAT_R = 1
    STAT_L = 2

    def __init__(self):
        super().__init__()
        self.eState = Enemy01.STAT_DOWN #MoveStateFlug
        self.XrangeMin = 0
        self.XrangeMax = Common.WIDTH
        
    #Set Move State
    def SetState(self, state):
        self.eState = state

    #Set Move Range
    def SetRange(self, min, max):
        self.XrangeMin = min
        self.XrangeMax = max

    def update(self):
        #print("Enemy Update Call")
        match self.eState:
            case Enemy01.STAT_DOWN:
                #print("Enemy Update Down Call")
                self._y += 2
                if self._y % 32 == 0:
                    if self._x < Common.WIDTH/2:
                        self.eState = Enemy01.STAT_R
                    elif self._x > Common.WIDTH/2:
                        self.eState = Enemy01.STAT_L
                pass
            case Enemy01.STAT_R:
                #print("Enemy Update Right Call")
                self._x += 2
                if self._x > self.XrangeMax:
                   self.eState = Enemy01.STAT_DOWN
                #pass
            case Enemy01.STAT_L:
                #print("Enemy Update Left Call")
                self._x -= 2
                if self._x < self.XrangeMin:
                    self.eState = Enemy01.STAT_DOWN
                #pass
                     
        if Common.HEIGHT< self._y:
            self.enable = False
            
    def draw(self):
        #print("Enemy Draw Call")

        if self._show:
            self.sp.spdraw(self._x, self._y)

