import pygame as pg
from settings import *
import operator

class Symbol(pg.sprite.Sprite): 
    def __init__(self, game, x, y):
        self._layer = 1
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.base_image = game.ground_img
        self.FONT = pg.font.Font('fonts/PublicPixel.ttf', int(TILESIZE * 0.6))
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rx = x 
        self.ry = y
        self.rect.x = self.rx 
        self.rect.y = self.ry

    def update_symbol(self, s):
        self.s = s
        self.txt_surface = self.FONT.render(s, True, BLACK)
        self.image = self.base_image.copy()
        self.image.blit(self.txt_surface, (7, 3))

    def update(self, dx=0, dy=0):
        self.rect.x = self.rx + dx*TILESIZE
        self.rect.y = self.ry + dy*TILESIZE

class Text():
    def __init__(self, game, x, y, h, w):
        self.symbols = dict()
        self.game = game
        for i in range(int(w // TILESIZE)):
            for j in range(int(h // TILESIZE)):
                self.create_symbol(x + j*TILESIZE, y + i*TILESIZE, s=' ')

        self.image = pg.Surface((h, w))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def rearrange_text(self):
        x_, y_ = -1, -1
        delete_list = []
        keys = self.symbols.keys()
        keys = sorted(keys, key=operator.itemgetter(1, 0)) #Сортируем
        for x, y in keys:
            if x_ != -1 and y_ != -1:
                if y_ == y and x_ != x - TILESIZE:
                    print(x_, y_, x, y)
                    delete_list.append(self.symbols[(x, y)])
                    x = x - TILESIZE

            x_, y_ = x, y
        
        for sym in delete_list:
            x, y, s = sym.rect.x, sym.rect.y, sym.s
            self.symbols.pop((x, y)).kill()
            self.create_symbol(x-TILESIZE, y, s)

    def delete_symbol(self, s):
        x = s.rx
        y = s.ry
        self.symbols.pop((x, y)).kill()
        self.rearrange_text()

    def create_symbol(self, x, y, s):
        self.symbols[(x, y)] = Symbol(self.game, x, y)
        self.symbols[(x, y)].update_symbol(s)


        

