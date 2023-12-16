import pygame as pg
from settings import *
import missions

class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, name="NPC1"):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.img = game.NPC_img
        self.rect = self.img.get_rect()
        self.rx = x 
        self.ry = y - TILESIZE // 2
        self.x = int(x // TILESIZE)
        self.y = int(y // TILESIZE)
        self.orientation = "Left"
        self.image = game.NPC_img
        self.text_image = game.NPC_text_img
        self.interactionflag = False
        self.interactions = self.game.NPC_data[name]["interactions"]
        print(self.interactions)
        self.int_i = 0
        

    def get_image(self):
        if self.orientation == "Left":
            self.image = pg.transform.flip(self.img, True, False)

    def say(self, textLines):
        self.game.textflag = True
        self.game.text_box.write_text(textLines, self.text_image)

    def inform(self, text, new_coords):
        self.say(text)
        self.move(new_coords[0], new_coords[1])

    def mission(self, mission, text, block, after_text):
        checker = getattr(missions, mission)
        if checker(self.game):
            self.say(after_text)
            return True
        self.say(text)
        self.game.player.move(dx=block[0], dy=block[1])
        return False


    def interaction(self):
        if self.interactionflag == False:
            self.interactionflag = True
            int_type = self.interactions[self.int_i]["type"]
            if int_type == "information":
                text = self.interactions[self.int_i]["text"]
                new_coords = self.interactions[self.int_i]["new_coords"]
                self.inform(text, new_coords)
                self.int_i += 1
            elif int_type == "mission":
                mission = self.interactions[self.int_i]["mission"]
                text = self.interactions[self.int_i]["text"]
                block = self.interactions[self.int_i]["block"]
                after_text = self.interactions[self.int_i]["after_text"]
                done = self.mission(mission, text, block, after_text)
                if done: 
                    self.int_i += 1

    def move(self, x, y):
        self.rx = x
        self.ry = y
        self.x = x // TILESIZE
        self.y = y // TILESIZE

    def update(self):
        self.rect.x = self.rx 
        self.rect.y = self.ry
        self.get_image()

class Chest(NPC):
    def __init__(self, game, x, y, item):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img = game.NPC_img
        self.rect = self.img.get_rect()
        self.rx = x 
        self.ry = y - TILESIZE // 2
        self.x = int(x // TILESIZE)
        self.y = int(y // TILESIZE)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_alpha(0) 
        self.text_image = game.chest_img
        self.interactionflag = False
        self.item = item
        self.empty = False
    
    def update(self):
        self.rect.x = self.rx 
        self.rect.y = self.ry
    
    def interaction(self):
        if self.interactionflag == False:
            self.interactionflag = True
            if not(self.empty):
                self.say(["Ты нашел в сундуке:", str(self.game.items_data[self.item])])
                self.empty = True
            else:
                self.say(["Сундук пуст."])
