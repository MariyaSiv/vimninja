import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    """
    Класс для игрока
    """
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self._layer = 3
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_alpha(100) 
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rx = x
        self.ry = y
        self.x = int(x // TILESIZE)
        self.y = int(y // TILESIZE)

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy) and not(self.go_beyond(dx, dy)):
            if (self.in_text() != None and self.in_symbol(dx, dy) != None or self.in_text(dx, dy) == None) or self.in_text() == None:
                self.rx += dx * TILESIZE
                self.ry += dy * TILESIZE
                self.x += dx
                self.y += dy
                

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.rect.collidepoint(self.rx+dx*TILESIZE+TILESIZE//2, 
                                      self.ry+dy*TILESIZE+TILESIZE//2):
                return True
        return False

    def in_symbol(self, dx=0, dy=0):
        text1 = self.in_text()
        if text1:
            for s in text1.symbols.values():
                if s.rect.collidepoint(self.rx + dx*TILESIZE, self.ry + dy*TILESIZE):
                    return s
        return None

    def in_text(self, dx=0, dy=0):
        for text in self.game.texts:
            if text.rect.collidepoint(self.rx + dx*TILESIZE, self.ry + dy*TILESIZE):
                return text
        return None
    
    def go_beyond(self, dx=0, dy=0):
        if self.x + dx < 1 or self.x + dx > self.game.map.tmxdata.width - 2:
            return True
        if self.y + dy < 1 or self.y + dy > self.game.map.tmxdata.height - 2:
            return True
        return False

    def update(self):
        self.rect.x = self.rx 
        self.rect.y = self.ry
        for NPC in self.game.NPCs:
            if self.x == NPC.x and self.y == NPC.y:
                print("interaction moment")
                NPC.interaction()
            elif self.x == self.game.chest1.x and self.y == self.game.chest1.y:
                self.game.chest1.interaction()
            else:
                NPC.interactionflag = False
                self.game.chest1.interactionflag = False

        

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

