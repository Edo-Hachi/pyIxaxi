# Phthon3 Program

from math import radians
from random import randint, random
from numpy import size
import pyxel
import Common
import Sprite
import Enemy
import math

ShipPosRecMax = 100 #自機の移動履歴レコード上限


#SinCosテーブル
SinTbl = []
CosTbl = []

#弾管理クラス
BulletList = []

#EnemyList Class
EnemyList = []
    
#GameCount :int=0 #ゲーム開始からのインターバルカウンタ

#消去フラグの立ったリスト要素を削除する
def CleanupList(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.enable == False:
            list.pop(i)
            print("Cleanup List")
        else:
            i += 1


class BULLET:
    def __init__(self, sx, sy, deg, spd, type):
        self.sx = sx    #開始座標
        self.sy = sy

        self.bx = sx    #現在座標
        self.by = sy

        self.spd = spd  #Speed
        self.type = type #Type


        #self.rad = math.atan2(ty-sy, tx-sx)
        self.deg= deg #math.degrees(self.rad)
        self.vx = CosTbl[self.deg]
        self.vy = SinTbl[self.deg]

        self.sp = Sprite.SPRITE()
        self.sp.spset(0, 16,16, 8,8, 16,16, 15)
        self.sp.spcolr(4,4,8,8)
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
            if type == 0:
                self.sp.spset(0, 16,16, 8,8, 0,16, 16)
            elif type == 1:
                self.sp.spset(0, 16,16, 8,8, 0,32, 16)

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

        self.roll = 0   #左右移動時のロール制御

        self.SpPl = Sprite.SPRITE()
        self.SpPl.spset(0, 16,16, 8, 8, 0,0, 15)
        self.SpPl.spshow(True)

    def draw(self):
        #pyxel.blt(self.px, self.py, 0, 0,0, 16,16, 15)
        if self.roll < 0:
            self.SpPl.spset(0, 16, 16, 8,8, 16,0, 15)
        elif self.roll > 0:
            self.SpPl.spset(0, -16, 16, 8,8, 16,0, 15)
        else:
            self.SpPl.spset(0, 16,16, 8, 8, 0,0, 15)
             
        self.SpPl.spdraw(self.px, self.py)

#オプション管理
class OPTION:
    #オプションの角度テーブル
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

        if 0 < self.Angle and AddAngle == -1:
            self.Angle -=1
        
        if self.Angle < 12  and AddAngle == 1:
            self.Angle +=1

        #print(self.Angle)

    #オプション表示
    def draw(self):
        self.Spl.spdraw(self.lox, self.loy)
        self.Spr.spdraw(self.rox, self.roy)

        #オプション光点L
        x1=self.lox
        y1=self.loy
        x2=x1 + CosTbl[OPTION.LOptAngleTbl[self.Angle]]*5
        y2=y1 + SinTbl[OPTION.LOptAngleTbl[self.Angle]]*5
        #pyxel.line(x1, y1, x2, y2,8)
        pyxel.circ(x2,y2,1,8)

        #オプション光点R
        x1=self.rox
        y1=self.roy
        x2=x1 + CosTbl[OPTION.ROptAngleTbl[self.Angle]]*5
        y2=y1 + SinTbl[OPTION.ROptAngleTbl[self.Angle]]*5
        #pyxel.line(x1, y1, x2, y2,8)
        pyxel.circ(x2,y2,1,8)

class clsGamePlay:
    def __init__(self):
        self.ship = SHIP()
        self.FpsCount=0
        self.BltTimer=0 #弾の発射間隔
        self.OptionLock=False   #オプション角度ロックフラグ

        self.Option = OPTION(0, 0)  #オプション管理クラス

        self.GameCount = 0 #ゲーム開始からのインターバルカウンタ

        self.EnemyDebugTimer = 0    #敵デバッグ用タイマー

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

    #--------------------------------------------------------------------------
    #Game Start Init Func
    def GameInit(self):
        self.GameCount = 0
        self.PosIndx=0  #自機のロータリーバッファポインタ
        self.OptPosIndx = -15  #オプションの座標は15インデックス遅れでついてくる
        #reset self.PosList
        for i in range(0,ShipPosRecMax+1):
            self.PosList[i].x = -1
            self.PosList[i].y = -1

    #--------------------------------------------------------------------------
    #更新処理
    def update(self):
        

        #キー入力(移動)
        vx=0;vy=0
        #Key input for movement
        #move up
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            vy=-1
            if self.FpsCount % 3 == 0: #3フレーム毎にオプションの角度を変更する
                self.Option.SetAngle(1)
        #move down
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            vy=1
            if self.FpsCount % 3 == 0: #3フレーム毎にオプションの角度を変更する
                self.Option.SetAngle(-1)
        #move left 
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            vx=-1
            if self.ship.roll > -10:
                self.ship.roll-=2
        #move right
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            vx=1
            if self.ship.roll < 10:
                self.ship.roll+=2

        #Adjustment of travel amount when moving diagonally
        cx=1; cy=1
        if vx != 0 and vy != 0: #ナナメ速度補正
            cx = 0.71
            cy = 0.71
        
        self.ship.px+=(vx * cx)
        self.ship.py+=(vy * cy)

        #自機の過去座標をロータリーバッファに保存
        #Save myship's movement path to rotary buffer　　
        self.PosList[self.PosIndx].x = self.ship.px
        self.PosList[self.PosIndx].y = self.ship.py
        self.PosIndx+=1
        if ShipPosRecMax-1 < self.PosIndx:
            self.PosIndx = 1

        #オプションのロータリーバッファ参照座標
        #Index of rotary buffer referenced by option
        self.OptPosIndx+=1
        if ShipPosRecMax-1 < self.OptPosIndx:
            self.OptPosIndx = 1

        #オプションの角度ロックを行うか？
        #Will the option maintain its current angle?

        if pyxel.btn(pyxel.KEY_LSHIFT):
            self.Option.AngleLock(True)
        else:
            self.Option.AngleLock(False)

        #オプションに現在座標設定
        #Options follow the trajectory of my ship.
        self.Option.SetPos(self.PosList[self.OptPosIndx].x, self.PosList[self.OptPosIndx].y)

        #Shot Bullet
        if pyxel.btn(pyxel.KEY_Z):
            if self.BltTimer <= 0:
                BulletList.append(BULLET(self.ship.px, self.ship.py, 270, 4, 0))

                BulletList.append(BULLET(self.Option.rox, self.Option.roy, OPTION.ROptAngleTbl[self.Option.Angle],3, 1))
                BulletList.append(BULLET(self.Option.lox, self.Option.loy, OPTION.LOptAngleTbl[self.Option.Angle],3, 1))

                self.BltTimer = 5   #Bullet Fire Timing per 5 frames
            else:
                self.BltTimer -= 1  #decrease Bullet Fire Timing

        for i in range(0, len(BulletList)):
            BulletList[i].update()

        if pyxel.btn(pyxel.KEY_E):
            #create new enemy object
            #if self.EnemyDebugTimer < 0:
            if self.GameCount % 10 == 0:
                enemy = Enemy.Enemy01()

                #enemy.SetPos(randint(0,Common.WIDTH), 32)
                enemy.SetPos(200, 0)

                enemy.SpDef(0, 16,16, 8,8, 0,32)
                enemy.SetShow(True)
                enemy.SetState(Enemy.Enemy01.STAT_R)
                enemy.SetRange(50, Common.WIDTH-50)

                EnemyList.append(enemy)
            #    self.EnemyDebugTimer = 10

            #else:
            #    self.EnemyDebugTimer -= 1


        for i in range(0, len(EnemyList)):
            EnemyList[i].update()
        
        #ship roll angle adjustment
        if self.ship.roll > 0:
            self.ship.roll -= 1
        elif self.ship.roll < 0:
            self.ship.roll += 1
        
        #print(self.ship.roll)

        #gabage collect  for bullet list
        CleanupList(BulletList)
        CleanupList(EnemyList)

        self.GameCount += 1  #ゲームカウント


    #Draw----------------------------------------------------------------------
    def draw(self):
        self.FpsCount+=1
        if 59<self.FpsCount:
            self.FpsCount=0

        pyxel.cls(0)

        #オプション描画
        if 0 < self.OptPosIndx: #オプションの表示座標は-15フレームから始めているので
            self.Option.draw()

        #Draw my ship
        self.ship.draw()

        #Draw My Ship bullet   
        for i in range(0, len(BulletList)):
            BulletList[i].draw()

        #Draw Enemy List
        for i in range(0, len(EnemyList)):
            EnemyList[i].draw()
