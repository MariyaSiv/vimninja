import pygame as pg
from settings import *


def check_mission_1(game):
    if game.chest1.empty:
        return True
    else:
        return False
    
