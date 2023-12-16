import pygame as pg
import pytmx
from settings import *

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            print(layer.name)
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name != "Walls2":
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, ((x) * self.tmxdata.tilewidth,
                                            (y) * self.tmxdata.tileheight))
    
    def newLayer(self, screen, camera):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Walls2":
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        tile_coords = ((x) * self.tmxdata.tilewidth,
                                       (y) * self.tmxdata.tileheight)
                        screen.blit(tile, camera.apply_dot(tile_coords))
    
    
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height, map_width, map_height):
        #camera offset
        self.offset = pg.math.Vector2()
        #camera box
        #self.camera = pg.Rect(0, 0, width, height)
        #self.width = width
        #self.height = height
        self.camera_borders = {'left': 5 * TILESIZE, 'right': 5 * TILESIZE, 'top': 5 * TILESIZE, 'bottom': 5 * TILESIZE}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = width - (self.camera_borders['left'] + self.camera_borders['right'])
        h = height - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera = pg.Rect(l,t,w,h)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.topleft - self.offset

    def apply_dot(self, coords):
        return (coords[0] - self.offset.x, coords[1] - self.offset.y)
    
    def apply_rect(self, rect):
        #return rect.move(self.camera.topleft)
        return rect.topleft - self.offset
    
    def update(self, target):
        if target.rect.left < self.camera.left:
            self.camera.left = max(target.rect.left, self.camera_borders['left'])
        if target.rect.right > self.camera.right:
            self.camera.right = min(target.rect.right, self.map_width - self.camera_borders['right'])
        if target.rect.top < self.camera.top:
            self.camera.top = max(target.rect.top, self.camera_borders['top'])
        if target.rect.bottom > self.camera.bottom:
            self.camera.bottom = min(target.rect.bottom, self.map_height - self.camera_borders['bottom'])

        #limit scrolling to map size
        self.offset.x = self.camera.left - self.camera_borders['left']
        self.offset.y = self.camera.top - self.camera_borders['top']

        return ((self.camera.top - self.camera_borders['top'])/ TILESIZE, (self.camera.bottom + self.camera_borders['bottom'])/ TILESIZE)
