import pygame
import random

from enum import Enum
from config import *


class RoomType(Enum):
    PADRAO = (17, 11)
    GRANDE = (34, 22)
    L_SHAPE = (34, 12)
    CURTO_H = (9, 11)
    CURTO_V = (11, 9)
    LONGO_H = (9, 22)
    LONGO_V = (22, 9)
    I_SHAPE_H = (34, 9)
    I_SHAPE_V = (9, 34)


class TreasureRoomType(Enum):
    T_PADRAO = (17, 11)
    T_CURTO_H = (9, 11)
    T_CURTO_V = (11, 9)


class Labirinto:
    def __init__(self, width_L, heigth_L):
        self.widht_L = width_L
        self.heogth_L = heigth_L

        self.common_type = random.choice(list(RoomType))
        self.is_locked = False
