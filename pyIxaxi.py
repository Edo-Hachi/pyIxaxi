# Phthon3 Program

#from numpy import True_
import pyxel
import Common
import Sprite
import Title
import GamePlay

VER='0.0.1'

TitleObj = Title.clsTitle()
GamePlayObj = GamePlay.clsGamePlay()

class App:
    #GState=DEF.GS_TITLE    #Game State

    def __init__(self):
        #DEF.GState = DEF.GS_TITLE
        #player
        # self.px=60
        # self.py=HEIGHT-16

        # self.vx = 0
        # self.vy = 0
        # self.initVy = -10
        # self.gravity = 1x
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

        pyxel.init(Common.WIDTH, Common.HEIGHT, "I.X.A.X.I. for Pyxel", Common.FPS)
        pyxel.load("./assets/ixaxi.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):

        match Common.GState:
            case Common.GS_PLAY:
                GamePlayObj.update()
                pass
            case Common.GS_TITLE:
                TitleObj.update()
                pass
            case Common.GS_GAMEOVER:
                pass
            case Common.GS_DEMO:
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

        match Common.GState:
            case Common.GS_PLAY:
                GamePlayObj.draw()
                pass
            case Common.GS_TITLE:
                TitleObj.draw()
                
                #if pyxel.btnp(pyxel.GAMEPAD1_AXIS_LEFTX):
                #    print("Pad Analog Left")
                #y= pyxel.btnp(pyxel.GAMEPAD1_AXIS_LEFTY)
                #print(x, y)


                #print("Draw Title")
                #objTitle.draw()
                pass
            case Common.GS_GAMEOVER:
                pass
            case Common.GS_DEMO:
                pass

App()
