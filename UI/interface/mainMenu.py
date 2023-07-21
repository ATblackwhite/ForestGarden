import pygame
from UI.button.playButton import PlayButton
from settings import Settings

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = Settings()
        self.background = pygame.transform.scale(pygame.image.load(r"sources\UI\mainMenu\mainMenu.png"),
                                                  (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        self.play_button = PlayButton(self.game)

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.play_button.draw_button()