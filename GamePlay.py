from math import radians
import pyxel
import Common
import math


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

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.ship.vy=-1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.ship.vy=1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.ship.vx=-1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.ship.vx=1
        
        self.ship.px+=self.ship.vx
        self.ship.py+=self.ship.vy

    def draw(self):
        pyxel.cls(1)
        self.ship.draw()

