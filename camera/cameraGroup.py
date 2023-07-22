import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    # 按照层数顺序绘制精灵
    def custom_draw(self):
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)