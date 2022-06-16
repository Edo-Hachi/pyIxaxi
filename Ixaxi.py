#from numpy import True_
import pyxel
import DEF
import ClassSprite
import FuncTitle
from enum import Enum

GState= DEF.GS_TITLE    #Game State

class App:

    def __init__(self):
        
        #player
        # self.px=60
        # self.py=HEIGHT-16

        # self.vx = 0
        # self.vy = 0
        # self.initVy = -10
        # self.gravity = 1
        # self.flgJmp=False

        # self.plsp = SpObj.sprite()
        # self.plsp.spset(0, 16,16, 0,0, 0,0, 15)
        # self.plsp.spshow(True)
        # self.plsp.spcolr(0,0,16,16)

        # #enemy
        # self.ensp = SpObj.sprite()
        # self.ensp.spset(0, 16,16, 0,0, 16,0, 15)
        # self.ensp.spshow(True)
        # self.ensp.spcolr(0,0,16,16)
        # self.ex = WIDTH+16
        
        # #floor
        # self.initFlr()

        pyxel.init(DEF.WIDTH, DEF.HEIGHT, "I.X.A.X.I. for Pyxel", DEF.FPS)
        pyxel.load("./assets/ixaxi.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):

        match GState:
            case DEF.GS_PLAY:
                pass
            case DEF.GS_TITLE:
                FuncTitle.update()
                pass
            case DEF.GS_GAMEOVER:
                pass
            case DEF.GS_DEMO:
                pass

        # if pyxel.btnp(pyxel.KEY_Q):
        #     pyxel.quit()

        # #LR
        # if pyxel.btn(pyxel.KEY_LEFT):
        #     self.px -= 2
        # if pyxel.btn(pyxel.KEY_RIGHT):
        #     self.px += 2

        # #Jump
        # if pyxel.btnp(pyxel.KEY_SPACE):
        #     if self.flgJmp == False:
        #         self.vy = self.initVy
        #         self.flgJmp = True
        
        # if self.flgJmp == True:
        #     self.py += self.vy
        #     self.vy += self.gravity

        # #プレイヤーのコリジョン領域を更新
        # self.plsp.spcolr_set(self.px, self.py)

        # #Enemy Move
        # self.ex-=3
        # if self.ex < -16:
        #     self.ex = WIDTH+16
        
        # #敵との接触判定
        # if self.plsp.sphitr(self.ensp)==True:
        #     print("Hit")

        # #床との接触判定
        # for i in range(len(FloorList)):
        #     if self.plsp.sphitr(FloorList[i])==True:
        #         #FloorList[i].show_collision_r(True)
        #         self.flgJmp = False
        #         #self.vy=0
        #         self.py=FloorList[i]._y-16
        #         #print(FloorList[i]._y)
        #         #print(self.py)
        #         break
                
    def draw(self):

        match GState:
            case DEF.GS_PLAY:
                pass
            case DEF.GS_TITLE:
                FuncTitle.draw()

                #print("Draw Title")
                #objTitle.draw()
                pass
            case DEF.GS_GAMEOVER:
                pass
            case DEF.GS_DEMO:
                pass

App()
