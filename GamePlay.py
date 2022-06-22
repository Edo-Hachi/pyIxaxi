from math import radians
from numpy import size
import pyxel
import Common
import Sprite
import math

ShipPosRecMax = 100 #自機の移動履歴レコード上限

#SinCosテーブル
SinTbl = []
CosTbl = []

#消去フラグの立ったリスト要素を削除する
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.enable == False:
            list.pop(i)
            #print("Delete bullet")
        else:
            i += 1

#弾管理クラス
BulletList = []

class BULLET:
    def __init__(self, sx, sy, deg, spd):
        self.sx = sx    #開始座標
        self.sy = sy

        self.bx = sx    #現在座標
        self.by = sy

        self.spd = spd  #Speed
        #self.rad = math.atan2(ty-sy, tx-sx)
        self.deg= deg #math.degrees(self.rad)
        self.vx = CosTbl[self.deg]
        self.vy = SinTbl[self.deg]

        self.sp = Sprite.SPRITE()
        self.sp.spset(0, 16,16, 8,8, 16,16,15)
        self.sp.spshow(True)

        self.enable = True

    def update(self):
        if self.enable == True:
            #self.by -= self.spd
            self.bx += self.vx * self.spd
            self.by += self.vy * self.spd

        if self.bx < -16:
            self.enable = False
        if Common.WIDTH+16 < self.bx:
            self.enable = False
        if self.by < -16:
            self.enable = False
        if Common.HEIGHT+16<self.by:
            self.enable = False

    def draw(self):
        if self.enable == True:
            #pyxel.blt(self.bx, self.by, 0, 0,16, 16,16, 15)
            self.sp.spdraw(self.bx, self.by)
            


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

        self.SpPl = Sprite.SPRITE()
        self.SpPl.spset(0, 16,16, 8, 8, 0,0, 15)
        self.SpPl.spshow(True)

    def draw(self):
        #pyxel.blt(self.px, self.py, 0, 0,0, 16,16, 15)
        self.SpPl.spdraw(self.px, self.py)

#オプション管理
class OPTION:
    #オプションの角度テーブル
    #OptAngleTbl = [90, 75, 60, 45, 30, 15, 0, (360-15), (360-30), (360-45), (360-60), (360-75), (360-90)]
    ROptAngleTbl = [(360-90), (360-75), (360-60), (360-45), (360-30), (360-15), 0, 15, 30, 45, 60, 75, 90]

    LOptAngleTbl = [(270), (180+75), (180+60), (180+45), (180+30), (180+15), 180, (180-15), (180-30), (180-45), (180-60), (180-75), 90]

    OFSX=16
    OFSY=8
    def __init__(self, px, py): #px, py=Player Ship Pos
        self.Angle = 6
        self.px = px
        self.py = py
        self.Lock = 0
        self.OptAngleTblSize = len(OPTION.ROptAngleTbl)

        self.Spl = Sprite.SPRITE()
        self.Spl.spset(0, 16,16, 8, 8, 32,0, 15)
        self.Spl.spshow(True)

        self.Spr = Sprite.SPRITE()
        self.Spr.spset(0, 16,16, 8, 8, 32,0, 15)
        self.Spr.spshow(True)

    
    def SetPos(self, px, py):
        self.px = px
        self.py = py

        self.lox = px - OPTION.OFSX #Left Option xpos
        self.rox = px + OPTION.OFSX #right Option xpos
        self.loy = self.roy = (py+OPTION.OFSY)

    def AngleLock(self, Lock:bool=False):
        self.Lock = Lock

    def AngleReset(self):
        self.Angle = 6

    def SetAngle(self, AddAngle): #AddAngle = +1 or -1
        if self.Lock == True:
            return

        #--------------------------------------------------------------------
        #print(self.OptAngleTblSize)

        if 0 < self.Angle and AddAngle == -1: #AddAngleself.OptAngle and self.FpsCount % 3 == 0: #3フレーム毎に角度を変更
            self.Angle -=1
        
        if self.Angle < 12  and AddAngle == 1:
            self.Angle +=1

        print(self.Angle)

    #オプション表示
    def draw(self):
        self.Spl.spdraw(self.lox, self.loy)
        self.Spr.spdraw(self.rox, self.roy)

        #オプション光点L
        x1=self.lox
        y1=self.loy
        x2=x1 + CosTbl[OPTION.LOptAngleTbl[self.Angle]]*5
        y2=y1 + SinTbl[OPTION.LOptAngleTbl[self.Angle]]*5
        pyxel.line(x1, y1, x2, y2,8)
        pyxel.circ(x2,y2,1,8)

        #オプション光点R
        x1=self.rox
        y1=self.roy
        x2=x1 + CosTbl[OPTION.ROptAngleTbl[self.Angle]]*5
        y2=y1 + SinTbl[OPTION.ROptAngleTbl[self.Angle]]*5
        pyxel.line(x1, y1, x2, y2,8)
        pyxel.circ(x2,y2,1,8)

class clsGamePlay:
    def __init__(self):
        self.ship = SHIP()
        self.FpsCount=0
        self.BltTimer=0 #弾の発射間隔
        self.OptionLock=False   #オプション角度ロックフラグ

        self.Option = OPTION(0, 0)  #オプション管理クラス

        #自機の移動軌跡を保存
        self.PosList = []
        for i in range(0,ShipPosRecMax+1):
            self.PosList.append(SHIPPOS(-1,-1))

        self.PosIndx=0  #自機のロータリーバッファポインタ
        self.OptPosIndx = -15  #オプションの座標は15インデックス遅れでついてくる

        #Sin Cos Table初期化
        for i in range(0,359):
            r = math.radians(i)
            SinTbl.append(math.sin(r))
            CosTbl.append(math.cos(r))
    

        #print (CosTbl[270] ,SinTbl[270] )

    #更新処理
    def update(self):
        
        #キー入力
        vx=0
        vy=0
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            vy=-1
            if self.FpsCount % 3 == 0: #3フレーム毎に角度を変更
                self.Option.SetAngle(1)
                #if 0< self.OptAngle and self.FpsCount % 3 == 0: #3フレーム毎に角度を変更
                #    self.OptAngle -=1
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            vy=1
            if self.FpsCount % 3 == 0: #3フレーム毎に角度を変更
                self.Option.SetAngle(-1)
            #if self.OptAngle < 12  and self.FpsCount % 3 == 0:
            #    self.OptAngle +=1
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            vx=-1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            vx=1

        cx=1
        cy=1
        if vx != 0 and vy != 0: #ナナメ速度補正
            cx = 0.71
            cy = 0.71
        self.ship.px+=(vx * cx)
        self.ship.py+=(vy * cy)

        #自機の過去座標をロータリーバッファに保存
        self.PosList[self.PosIndx].x = self.ship.px
        self.PosList[self.PosIndx].y = self.ship.py
        self.PosIndx+=1
        if ShipPosRecMax-1 < self.PosIndx:
            self.PosIndx = 1

        #オプションのロータリーバッファ参照座標
        self.OptPosIndx+=1
        if ShipPosRecMax-1 < self.OptPosIndx:
            self.OptPosIndx = 1

        #オプションの角度ロックを行うか？
        if pyxel.btn(pyxel.KEY_X):
            self.Option.AngleLock(True)
        else:
            self.Option.AngleLock(False)

        #オプションに現在座標設定
        self.Option.SetPos(self.PosList[self.OptPosIndx].x, self.PosList[self.OptPosIndx].y)

        #弾発射

#    class BULLET2:
#    def __init__(self, sx, sy, deg, spd):

        if pyxel.btn(pyxel.KEY_Z):
            if self.BltTimer <= 0:
                #BulletList.append(BULLET(self.ship.px, self.ship.py, 4))
                BulletList.append(BULLET(self.ship.px, self.ship.py, 270, 4))

                BulletList.append(BULLET(self.Option.rox, self.Option.roy, OPTION.ROptAngleTbl[self.Option.Angle],3))
                BulletList.append(BULLET(self.Option.lox, self.Option.loy, OPTION.LOptAngleTbl[self.Option.Angle],3))

    # OptAngleTbl = [(360-90), (360-75), (360-60), (360-45), (360-30), (360-15), 0, 15, 30, 45, 60, 75, 90]

    # OFSX=16
    # OFSY=8
    # def __init__(self, px, py): #px, py=Player Ship Pos
    #     self.Angle = 6

                self.BltTimer = 5   #Bullet Fire Timing
            else:
                self.BltTimer -= 1

        for i in range(0, len(BulletList)):
            BulletList[i].update()

        #debug
        cleanup_list(BulletList)


    def draw(self):
        self.FpsCount+=1
        if 59<self.FpsCount:
            self.FpsCount=0

        pyxel.cls(1)

        #オプション描画
        if 0 < self.OptPosIndx: #オプションの表示座標は-15フレームから始めているので
            self.Option.draw()

        #自機描画
        self.ship.draw()

        #自弾描画       
        for i in range(0, len(BulletList)):
            BulletList[i].draw()
    


