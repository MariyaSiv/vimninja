# content of test_sysexit.py
import pytest

from main import Game

import pygame as pg
from settings import *


def test_game_init():
    """
    Что игра инициализируется
    """
    pg.init()
    g = Game()


def test_start_position():
    """
    Стартовая позиция игрока
    """
    pg.init()
    g = Game()
    g.new(1)

    player_y = g.player.y
    assert player_y == 2

def test_player_move():
    """
    Что игрок движется
    """
    pg.init()
    g = Game()
    g.new(1)
    player_y_start = g.player.y
    g.player.move(dy=1)
    player_y = g.player.y
    assert player_y_start + 1 == player_y
