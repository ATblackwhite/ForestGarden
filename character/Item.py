import sys
sys.path.append('..')
from sources.Item import ID_Item_Table
sys.path.remove('..')
import pygame


class Item:

    def __init__(self, name):
        self.item_name = name
        self.icon_name = self.item_name + ".img"
        self.icon_location = ID_Item_Table.ID_Item_Table[self.icon_name]
        self.description_name = self.item_name + ".des"
        self.description_location = ID_Item_Table.ID_Item_Table[self.description_name]
        self.icon = pygame.image.load(self.icon_location)
        self.icon_backpack = pygame.transform.scale(self.icon, (80, 80))
        self.icon_inventory = pygame.transform.scale(self.icon, (50, 50))
        self.description_line = open(self.description_location, "r")
        self.description = self.description_line.read()
        self.handled = False
        self.chosen = False

    def presentInBackPack(self, space, isBackpack):
        self.space = space
        self.posx = self.space.posx+6
        self.posy = self.space.posy
        if isBackpack:
            self.icon = self.icon_backpack
        else:
            self.icon = self.icon_inventory

    def display(self):
        self.space.backpack.player.screen.blit(self.icon, (self.posx, self.posy))

    #New
    def item_use(self, interaction_point):
        match self.item_name:
            case "Hoe":
                self.space.backpack.player.map_grid.plough(interaction_point)
                print("Hoe used")

