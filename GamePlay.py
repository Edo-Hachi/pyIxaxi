from math import radians
import pyxel
import Common
import math

BulletList = []

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.enable == False:
            list.pop(i)
        else:
            i += 1


class BULLET:
    def __init__(self, x, y, spd):
        self.bx = x
        self.by = y
        self.spd = spd
        self.enable = True
    
    def update(self):
        if self.enable == True:
            self.by -= self.spd

        if self.by < -16:
            self.enable = False

    def draw(self):
        if self.enable == True:
            pyxel.blt(self.bx, self.by, 0, 0,16, 16,16, 15)

class SHIP:
    def __init__(self):
        self.px=100
        self.py=100
        self.vx=0
        self.vy=0

        self.sintbl = []
        self.costbl = []

        for i in range(0,359):
            r = math.radians(i)
            self.sintbl.append(math.sin(r))
            self.costbl.append(math.cos(r))

    def draw(self):
        pyxel.blt(self.px, self.py, 0, 0,0, 16,16, 15)

class clsGamePlay:

    def __init__(self):
        self.ship = SHIP()
        self.FpsCount=0
        self.BltTimer=0

    def update(self):
        vx=0
        vy=0
        if pyxel.btn(pyxel.KEY_UP):
            vy=-1
        if pyxel.btn(pyxel.KEY_DOWN):
            vy=1
        if pyxel.btn(pyxel.KEY_LEFT):
            vx=-1
        if pyxel.btn(pyxel.KEY_RIGHT):
            vx=1

        
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            vy=-1
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            vy=1
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            vx=-1
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            vx=1
        
        cx=1
        cy=1
        if vx != 0 and vy != 0: #ナナメ補正
            cx = 0.71
            cy = 0.71
        self.ship.px+=(vx * cx)
        self.ship.py+=(vy * cy)

        if pyxel.btn(pyxel.KEY_SPACE):
            if self.BltTimer <= 0:
                BulletList.append(BULLET(self.ship.px, self.ship.py, 4))
                self.BltTimer = 5   #Bullet Fire Timing
            else:
                self.BltTimer -= 1


        for i in range(0, len(BulletList)):
            BulletList[i].update()

        cleanup_list(BulletList)

    def draw(self):
        self.FpsCount+=1
        if 59<self.FpsCount:
            self.FpsCount=0
        #print(self.FpsCount)

        pyxel.cls(1)
        self.ship.draw()

        #print(len(BulletList))
        for i in range(0, len(BulletList)):
            BulletList[i].draw()
    


