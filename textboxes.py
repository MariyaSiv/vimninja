import pygame as pg
from settings import *

#pg.init()
#screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = GREEN

class InputBox:

    def __init__(self, game, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.game = game

        self.FONT = pg.font.Font('fonts/PublicPixel.ttf', int(TILESIZE * 0.5))
        self.txt_surface = self.FONT.render(text, True, BLACK)
        self.active = True


    def handle_event(self, event):
        #if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            #if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                #self.active = not self.active
            #else:
                #self.active = False
            # Change the current color of the input box.
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return_text = self.text
                self.text = ':'
                self.txt_surface = self.FONT.render(self.text, True, BLACK)
                return return_text
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = self.FONT.render(self.text, True, BLACK)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        pg.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.

class TextBox:

    def __init__(self, game, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.game = game

        self.FONT = pg.font.Font('fonts/PublicPixel.ttf', int(TILESIZE * 0.6))
        self.txt_surface = self.FONT.render(text, True, BLACK)
        self.active = True
        self.dialog_box = game.dialog_img

    def handle_event(self, event):
        self.color = COLOR_ACTIVE
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return False
            if event.key == pg.K_ESCAPE:
                return False
        return True

    def split_lines(self, text):
        pass
    
    def write_text(self, splitLines, image):
        self.image = image
        self.paragraphSurface = pg.Surface((self.rect.width, self.rect.height))
        #Set colorkey to fake transparent paragraph surface
        self.paragraphSurface.fill((255, 255, 255))
        self.paragraphSurface.set_colorkey((255, 255, 255))

        fontSize = self.FONT.get_height()
        for idx, line in enumerate(splitLines):
            currentTextline = self.FONT.render(line, True, BLACK)
            currentPostion = (0, idx * fontSize)
            self.paragraphSurface.blit(currentTextline, currentPostion)

    def update(self):
        pass
        # Resize the box if the text is too long.
        #width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        s = pg.Surface((WIDTH,HEIGHT))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill(BLACK)           # this fills the entire surface
        screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
        screen.blit(self.dialog_box, (self.rect.x+12, self.rect.y+12))
        screen.blit(self.image, (self.rect.x + TILESIZE, self.rect.y + TILESIZE))
        screen.blit(self.paragraphSurface, (self.rect.x+TILESIZE*7, self.rect.y+TILESIZE+10))
        # Blit the rect.
 
