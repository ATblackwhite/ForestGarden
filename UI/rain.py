import pygame
from settings import *
from sprites.drop import Drop
from random import choice, randint

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = [pygame.image.load('asset/rain/drops/' + str(i) + '.png').convert_alpha() for i in range(1, 3)]
        self.rain_floor = [pygame.image.load('asset/rain/floor/' + str(i) + '.png').convert_alpha() for i in range(1, 3)]
        self.floor_w, self.floor_h = pygame.image.load('asset/map.png').get_size()

    def create_floor(self):
        Drop(
            surf=choice(self.rain_floor),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor']
        )

    def create_drops(self):
        Drop(
            surf=choice(self.rain_drops),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain drops']
        )

    def update(self):
        self.create_drops()
        self.create_floor()
        self.create_drops()