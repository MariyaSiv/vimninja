import pygame as pg
import sys
import json
from os import path

from settings import *
from sprites import *
from NPC import *
from textboxes import *
from tilemap import *
from borders import *

from text import *
from modes import *

'''
        Summary line.
          
        Extended description of function.

        :param int arg1: Description of arg1.
        :param str arg2: Description of arg2.
        :raise: ValueError if arg1 is equal to arg2
        :return: Description of return value
        :rtype: bool

        :example:

'''

class Game:
    def __init__(self):
        '''
        Инициализация игры.

        Создание screen и внутренних часов. Настройка set_repeat.
        '''

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100) #miliseconds


    def load_data(self, lesson):
        '''
        Загружает данные об уровне, изображения и карту.

        Parameters
        ----------
        lesson : int
            Номер уровня
        '''

        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        self.map = TiledMap(path.join(map_folder, 'map'+str(lesson)+'.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.NPC_text_img = pg.image.load(path.join(img_folder, "monster.jpg")).convert_alpha()
        self.dialog_img = pg.image.load(path.join(img_folder, "dialog.png")).convert_alpha()
        self.NPC_img = pg.image.load(path.join(img_folder, "Dude_Monster.png"))
        
        self.ground_img = pg.image.load(path.join(img_folder, "stone_text.png"))
        self.chest_img = pg.image.load(path.join(img_folder, "chest.jpg"))

        json_file = './levels/level'+str(lesson)+'/interactions.json'
        with open(json_file) as json_data:
            self.NPC_data = json.load(json_data)
        json_file = './levels/level'+str(lesson)+'/items.json'
        with open(json_file) as json_data:
            self.items_data = json.load(json_data)

    def new(self, lesson):
        '''
        Инициализация уровня, создание основных объектов игры.

        Parameters
        ----------
        lesson : int
            Номер уровня
        '''
        self.load_data(lesson)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.texts = []
        self.NPCs = []
       
        for tile_object in self.map.tmxdata.objects:
            print(self.map.tmxdata.properties)
            if tile_object.name == "Player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "NPC":
                self.NPCs.append(NPC(self, tile_object.x, tile_object.y, "NPC1"))
            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == "item":
                self.chest1 = Chest(self, tile_object.x, tile_object.y, "test_item") 
            if tile_object.properties:
                if tile_object.properties["Text"]:
                    self.texts.append(Text(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)) 
        
        self.camera = Camera(WIDTH, HEIGHT, self.map.width, self.map.height)
        self.border = Border(self)
        self.input_box = InputBox(self, TILESIZE, HEIGHT-TILESIZE, 300, TILESIZE, ':')
        self.text_box = TextBox(self, TILESIZE*3, HEIGHT - TILESIZE*9, 
                                      WIDTH - TILESIZE*6, TILESIZE*7, 
                                      text = "")

        self.textflag = False # Режим text_box, например, диалог с NPC
        self.insertmode = False #Режим Insert 
        self.inputflag = False # Чтобы отдельно контролировать input
        

    def run(self):
        '''
        Level loop. Чтобы закончить уровень - self.playing = False
        '''
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        '''
        Выход из игры.
        '''
        pg.quit()
        sys.exit()

    def update(self):
        '''
        Обновляет события на экране
        '''
        # update portion of the game loop
        if self.inputflag:
            self.input_box.update()
        #elif self.textflag:
        #    self.text_box.update()
        else:
            self.all_sprites.update()
            camera_limits = self.camera.update(self.player)
            camera_limits = [int(i) for i in camera_limits]
            self.border.update(range(camera_limits[0] + 1, camera_limits[1] - 1), self.player)

    def draw_grid(self):
        '''
        Рисует сетку.
        '''
        for y in range(BORDERWIDTH*2, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (BORDERWIDTH, y), (WIDTH - BORDERWIDTH, y))
        for x in range(BORDERWIDTH*2, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, BORDERWIDTH), (x, HEIGHT - BORDERWIDTH))
        
        pg.draw.line(self.screen, BLACK, (BORDERWIDTH, BORDERWIDTH), (BORDERWIDTH, HEIGHT - BORDERWIDTH))
        pg.draw.line(self.screen, BLACK, (BORDERWIDTH, BORDERWIDTH), (WIDTH - BORDERWIDTH, BORDERWIDTH))
        pg.draw.line(self.screen, BLACK, (BORDERWIDTH, HEIGHT - TILESIZE), (WIDTH - BORDERWIDTH, HEIGHT - TILESIZE))
        pg.draw.line(self.screen, BLACK, (WIDTH - TILESIZE, BORDERWIDTH), (WIDTH-TILESIZE, HEIGHT - BORDERWIDTH))

    def draw(self):
        '''
        Отображает спрайты на экране, отрисовывает объекты.
        '''
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            #print(sprite, sprite.rect.topleft, sprite._layer)
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.map.newLayer(self.screen, self.camera)
        
        self.draw_grid()
        if self.textflag:
            self.text_box.draw(self.screen)
        
        self.border.draw()

        if self.inputflag:
            self.input_box.draw(self.screen)
        pg.display.flip()

    def events(self):
        '''
        Главные обработчик событий.
        '''
        for event in pg.event.get():
            if self.inputflag:
                return_text = self.input_box.handle_event(event)
                if return_text != None:
                    if return_text.isdigit():
                        self.player.y = int(return_text)
                    self.inputflag = False
            elif self.textflag:
                self.textflag = self.text_box.handle_event(event)
            elif self.insertmode:
                self.insertmode = InsertModeHandle(event, self)
                self.border.color = YELLOW
            else:
                self.border.color = GREEN
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.playing = False
                    if event.key == pg.K_h:
                        self.player.move(dx=-1)
                    if event.key == pg.K_l:
                        self.player.move(dx=1)
                    if event.key == pg.K_k:
                        self.player.move(dy=-1)
                    if event.key == pg.K_j:
                        print(event, self.player.x, self.player.y)
                        self.player.move(dy=1) 
                    if event.key == pg.K_i:
                        self.insertmode = True
                    if event.key == pg.K_1:
                        self.inputflag = True
                    if event.key == pg.K_g:
                        if self.previousKEYDOWN == pg.K_g:
                            self.player.y = 1
                    self.previousKEYDOWN = event.key
    
    def show_start_screen(self):
        '''
        Показывает основное меню.

        Returns
        ----------
        int
            Номер уровня, который выбрал игрок
        '''
        lesson = 1
        end = True
        while end:
            for event in pg.event.get(): 
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        lesson = max(1, lesson - 1)
                    if event.key == pg.K_RIGHT:
                        lesson = min(LEVELS_N, lesson + 1)
                    if event.key == pg.K_SPACE:
                        end = False

            self.screen.fill((0, 0, 0))
            font = pg.font.Font('fonts/PublicPixel.ttf', 35)
            font_little = pg.font.Font('fonts/PublicPixel.ttf', 15)
            title = font.render('Vim Ninja', True, (255, 255, 255))
            start_button = font.render('< Lesson #' + str(lesson) + ' >', True, (255, 255, 255))
            info = font_little.render('<space> to start, <arrow keys> to choose lesson', True, (255, 255, 255))
            
            self.screen.blit(title, (WIDTH/2 - title.get_width()/2, 
                            HEIGHT/2 - title.get_height()/2))
            self.screen.blit(start_button, (WIDTH/2 - start_button.get_width()/2, 
                                       HEIGHT/2 + start_button.get_height()/2))
            self.screen.blit(info, (WIDTH/2 - info.get_width()/2, 
                                       HEIGHT/2 + info.get_height()/2 + 100))
            pg.display.update()
        return lesson
        

    def show_go_screen(self):
        pass

def main():
    '''
    Создает объект игры.
    '''
    g = Game()
    while(True):
        lesson = g.show_start_screen()
        g.new(lesson)
        g.run()
        g.show_go_screen()

if __name__ == "__main__":
    main()
