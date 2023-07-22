from sprites.generic import Generic
import pygame
from settings import *

class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups, LAYERS['main'])