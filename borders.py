import pygame as pg
from settings import *

class Border(pg.sprite.Sprite):
    def __init__(self, game):
        self.screen = game.screen
        self.letters = []
        self.color = GREEN

    def update(self, n_range, player):
        self.letters = []
        i = 1
        for number in n_range:
            self.letters.append(Letter(0, i, str(number)))
            i += 1
        FONT = pg.font.Font('fonts/PublicPixel.ttf', int(TILESIZE * 0.5))
        self.coords = FONT.render(str(player.x) + ":" + str(player.y), True, 'Black')
        #self.coords_rect = self.coords.get_rect()

    def draw(self):
        pg.draw.rect(self.screen, self.color, [0, 0, WIDTH, BORDERWIDTH])
        pg.draw.rect(self.screen, self.color, [0, HEIGHT-BORDERWIDTH, WIDTH, BORDERWIDTH])
        pg.draw.rect(self.screen, self.color, [0, 0, BORDERWIDTH, HEIGHT])
        pg.draw.rect(self.screen, self.color, [WIDTH-BORDERWIDTH, 0, BORDERWIDTH, HEIGHT])
        for l in self.letters:
            self.screen.blit(l.image, (l.rect.left + 5, l.rect.top + 10))
        self.screen.blit(self.coords, (WIDTH-150, HEIGHT-TILESIZE+5))

class Letter(pg.sprite.Sprite):
    def __init__(self, x, y, letter):
        FONT = pg.font.Font('fonts/PublicPixel.ttf', int(TILESIZE * 0.4))
        letter = letter if len(letter) == 2 else '0' + letter
        test_surface = FONT.render(letter, True, 'Black')
        self.image = test_surface
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

