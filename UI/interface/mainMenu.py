import pygame
from UI.button.playButton import PlayButton
from settings import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.background = pygame.transform.scale(pygame.image.load(r"sources\UI\mainMenu\mainMenu.png"),
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.play_button = PlayButton(self.game)

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.play_button.draw_button()