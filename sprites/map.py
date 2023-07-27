from settings import *
from sprites.generic import Generic
import pygame

class Map(Generic):
    def __init__(self, pos, surf, groups, z):
        self.image_frame = surf
        self.index = 0
        super().__init__(pos, self.image_frame[self.index], groups, z)
        self.last_time = pygame.time.get_ticks()

    def change(self, current_season):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 100:
            self.last_time = current_time
            if current_season == 1:
                if self.index > 0:
                    self.index -= 1
                self.image = self.image_frame[self.index]
                self.z = LAYERS['ground']
            elif current_season == 4:
                if self.index < 4:
                    self.index += 1
                self.image = self.image_frame[self.index]
                self.z = LAYERS['ground plant']