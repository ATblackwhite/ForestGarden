from sprites.generic import Generic
from sprites.particle import Particle
import pygame
from settings import *
from camera.cameraGroup import CameraGroup

class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups, LAYERS['main'])

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.8)
        # 需要让hitbox处于树根部分
        self.hitbox.bottom = self.rect.bottom
        self.health = 3
        self.alive = True
        self.stump_image = pygame.image.load(r"asset\objects\fruitTrees__036.png").convert_alpha()
        for group in self.groups():
            if isinstance(group, CameraGroup):
                self.all_sprites = group

    def damage(self):
        if self.alive:
            self.health -= 1

            Particle(
                pos=self.rect.topleft,
                surf=self.image,
                groups=self.all_sprites,  # self.groups()[1]是all_sprites组
                z=LAYERS['fruit']
            )
            if self.health <= 0:
                self.alive = False
                self.image = self.stump_image
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.9, -self.rect.height * 0.6)
