import pygame as pg
from settings import *

def InsertModeHandle(event, game):
    text = game.player.in_text()
    if text == None:
        return False

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            return False
        elif event.key == pg.K_BACKSPACE:
            s = game.player.in_symbol()
            if s:
                if game.player.in_text(dx=-1):
                    text.delete_symbol(s)
                    game.player.move(dx=-1)
                else:
                    s.update_symbol(' ')
        else:
            s = game.player.in_symbol()
            if s:
                s.update_symbol(event.unicode)
                if game.player.in_text(dx=1):
                    if game.player.in_symbol(dx=1):
                        game.player.move(dx=1)
                    else:
                        text.create_symbol(game.player.rx + TILESIZE, game.player.ry, ' ')
                        game.player.move(dx=1) 
                        game.player.move(dx=1) 
    return True
