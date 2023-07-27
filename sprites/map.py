from settings import *
from sprites.generic import Generic

class Map(Generic):
    def __init__(self, pos, surf, groups, z):
        self.image_frame = surf
        super().__init__(pos, self.image_frame[0], groups, z)

    def change(self, current_season):
        if current_season == 1:
            self.image = self.image_frame[0]
            self.z = LAYERS['ground']
        elif current_season == 4:
            self.image = self.image_frame[1]
            self.z = LAYERS['ground plant']