from math import radians
import pyxel
import Common
import math

ShipPosRecMax = 100


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.enable == False:
            list.pop(i)
        else:
            i += 1

#SinCosテーブル
SinTbl = []
CosTbl = []

#弾管理クラス
BulletList = []
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
            print("shot draw")


#座標管理
class SHIPPOS:
    def __init__(self, x, y):
        self.x=x
        self.y=y

#自機管理クラス
class SHIP:
    def __init__(self):
        self.px=100
        self.py=100
        self.vx=0
        self.vy=0


    def draw(self):
        pyxel.blt(self.px, self.py, 0, 0,0, 16,16, 15)

# class OPTION:
#     def __init__(self):
#         self.ex=0
#         self.ey=0




class clsGamePlay:

    def __init__(self):
        self.ship = SHIP()
        self.FpsCount=0
        self.BltTimer=0

        #自機の移動軌跡を保存
        self.PosList = []
        for i in range(0,ShipPosRecMax+1):
            self.PosList.append(SHIPPOS(-1,-1))

        self.PosIndx=0  #自機のロータリーバッファポインタ
        self.OptPosIndx = -10   #オプションの座標は10インデックス遅れでついてくる

        for i in range(0,359):
            r = math.radians(i)
            SinTbl.append(math.sin(r))
            CosTbl.append(math.cos(r))

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

        #自機の過去座標をロータリーバッファに保存
        self.PosList[self.PosIndx].x = self.ship.px
        self.PosList[self.PosIndx].y = self.ship.py
        self.PosIndx+=1
        if ShipPosRecMax-1 < self.PosIndx:
            self.PosIndx = 0

        #オプションのロータリーバッファ参照座標
        self.OptPosIndx+=1
        if ShipPosRecMax-1 < self.OptPosIndx:
            self.OptPosIndx = 1


        if pyxel.btn(pyxel.KEY_SPACE):
            if self.BltTimer <= 0:
                BulletList.append(BULLET(self.ship.px, self.ship.py, 4))
                self.BltTimer = 5   #Bullet Fire Timing
            else:
                self.BltTimer -= 1

        for i in range(0, len(BulletList)):
            BulletList[i].update()

        #cleanup_list(BulletList)

    def draw(self):
        self.FpsCount+=1
        if 59<self.FpsCount:
            self.FpsCount=0
        #print(self.FpsCount)

        pyxel.cls(1)
        self.ship.draw()

        #オプション表示

        if 0 < self.OptPosIndx:
#            if self.PosList[self.OptPosIndx].x != -1 and self.PosList[self.OptPosIndx].y != -1:
            pyxel.blt(self.PosList[self.OptPosIndx].x - 24, self.PosList[self.OptPosIndx].y+8, 0, 32,0, 16,16, 15)
            pyxel.blt(self.PosList[self.OptPosIndx].x + 24, self.PosList[self.OptPosIndx].y+8, 0, 32,0, 16,16, 15)
            #self.PosList[self.OptPosIndx].x = self.PosList[self.OptPosIndx].y = -1

        
        for i in range(0, len(BulletList)):
            BulletList[i].draw()
    


