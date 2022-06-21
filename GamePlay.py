from math import radians
from numpy import size
import pyxel
import Common
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
            print("Delete bullet")
        else:
            i += 1

#弾管理クラス
BulletList = []
# class BULLET:
#     def __init__(self, x, y, spd):
#         self.bx = x
#         self.by = y
#         self.spd = spd
#         self.enable = True
    
#     def update(self):
#         if self.enable == True:
#             self.by -= self.spd

#         if self.by < -16:
#             self.enable = False

#     def draw(self):
#         if self.enable == True:
#             pyxel.blt(self.bx, self.by, 0, 0,16, 16,16, 15)
#             #print("shot draw")

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
            pyxel.blt(self.bx, self.by, 0, 0,16, 16,16, 15)


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

#オプション管理
class OPTION:
    #オプションの角度テーブル
    #OptAngleTbl = [90, 75, 60, 45, 30, 15, 0, (360-15), (360-30), (360-45), (360-60), (360-75), (360-90)]
    OptAngleTbl = [(360-90), (360-75), (360-60), (360-45), (360-30), (360-15), 0, 15, 30, 45, 60, 75, 90]

    OFSX=16
    OFSY=8
    def __init__(self, px, py): #px, py=Player Ship Pos
        self.Angle = 6
        self.px = px
        self.py = py
        self.Lock = 0

        self.OptAngleTblSize = len(OPTION.OptAngleTbl)
    
    def SetPos(self, px, py):
        self.px = px
        self.py = py

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

    #オプション表示
    def draw(self):
        pyxel.blt(self.px - OPTION.OFSX, self.py+OPTION.OFSY, 0, 32,0, 16,16, 15)
        pyxel.blt(self.px + OPTION.OFSX, self.py+OPTION.OFSY, 0, 32,0, 16,16, 15)
            
        #オプション光点L
        x1=self.px - OPTION.OFSX + 8
        y1=self.py + OPTION.OFSY + 8

        x2=x1 - CosTbl[OPTION.OptAngleTbl[self.Angle]]*5
        y2=y1 + SinTbl[OPTION.OptAngleTbl[self.Angle]]*5
        pyxel.circ(x2,y2,1,8)
        #pyxel.line(x1,y1,x2,y2,8)

        #オプション光点R
        x1=self.px + OPTION.OFSX + 8
        x2=x1 + CosTbl[OPTION.OptAngleTbl[self.Angle]]*5
        pyxel.circ(x2,y2,1,8)
        #pyxel.line(x1,y1,x2,y2,8)

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
    


