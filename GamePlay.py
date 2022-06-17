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
        if vx != 0 and vy != 0:
            cx = 0.71
            cy = 0.71
        
        self.ship.px+=(vx * cx)
        self.ship.py+=(vy * cy)

    def draw(self):
        pyxel.cls(1)
        self.ship.draw()

