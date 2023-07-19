import os
import sys
sys.path.append('..')
from sources.Item import ID_Item_Table
sys.path.remove('..')
import pygame


class Item:

    def __init__(self, ID):
        self.item_id = str(ID)
        self.icon_name = self.item_id + ".img"
        self.icon_location = ID_Item_Table.ID_Item_Table[self.icon_name]
        self.description_name = self.item_id + ".des"
        self.description_location = ID_Item_Table.ID_Item_Table[self.description_name]
        self.icon = pygame.image.load(self.icon_location)
        self.description_line = open(self.description_location, "r")
        self.description = self.description_line.read()
        self.handled = False
        self.chosen = False

    def presentInBackPack(self, space):
        self.space = space
        self.posx = self.space.posx+3
        self.posy = self.space.posy
        self.icon = pygame.transform.scale(self.icon, (40, 40))

    def display(self):
        self.space.backpack.player.screen.blit(self.icon, (self.posx, self.posy))
