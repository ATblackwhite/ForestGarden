from sprites.generic import Generic
import pygame
from settings import *

class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups, LAYERS['main'])
        self.rect = self.image.get_rect(midbottom=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.6)
        # 需要让hitbox处于树根部分
        self.hitbox.bottom = self.rect.bottom
        self.health = 3
        self.alive = True
        self.stump_image = pygame.image.load(r"asset\objects\fruitTrees__036.png").convert_alpha()

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            self.alive = False
            self.image = self.stump_image
