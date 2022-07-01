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
            case Common.GS_PLAY_INIT:
                GamePlayObj.GameInit()
                Common.GState = Common.GS_PLAY

            case Common.GS_GAMEOVER:
                pass
            case Common.GS_DEMO:
                pass

    def draw(self):

        match Common.GState:
            case Common.GS_PLAY:
                GamePlayObj.draw()
                pass
            case Common.GS_TITLE:
                TitleObj.draw()
                pass
            case Common.GS_GAMEOVER:
                pass
            case Common.GS_DEMO:
                pass

App()
