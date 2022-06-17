#from curses.ascii import GS
import pyxel
import Common

class clsTitle:
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_S):
            print("Push S")
            Common.GState = Common.GS_PLAY
            #return DEF.GS_PLAY
            #Ixaxi.GState=DEF.GS_PLAY    #Game State
            
            pass

    def draw(self):
        pyxel.cls(1)
        pyxel.text(100,100,"I.X.A.X.I.", 7)
        pyxel.text(100,120,"Press [Q] QuitGame.", 7)

        pyxel.blt(0,50, 2, 0,0, 191,32, 15)
