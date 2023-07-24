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
        self.num = 1

    def presentInBackPack(self, space, isBackpack):
        self.space = space
        self.posx = self.space.posx+6
        self.posy = self.space.posy
        if isBackpack:
            self.icon = self.icon_backpack
        else:
            self.icon = self.icon_inventory

        self.player = self.space.backpack.player

    def display(self, isInventory):
        self.player.screen.blit(self.icon, (self.posx, self.posy))
        if self.num > 1:
            font = pygame.font.Font('sources/UI/UIPack/Font/kenvector_future.ttf', 24)
            number = font.render(str(self.num), True, (0, 0, 0))
            if isInventory:
                self.player.screen.blit(number, (self.posx+50-20, self.posy+50-20))
            else:
                self.player.screen.blit(number, (self.posx+80-15, self.posy+80-25))

    #New
    def item_use(self, interaction_point):
        match self.item_name:
            case "Hoe":
                self.player.map_grid.plough(interaction_point)
                self.player.useItemAnimate(self.item_name)

            case "Pot":
                self.player.map_grid.water(interaction_point)
                self.player.useItemAnimate(self.item_name)

            case "Axe":
                for i in self.player.tree_group:
                    if i.rect.collidepoint(self.player.interaction_point):
                        i.damage()

                self.player.useItemAnimate(self.item_name)

        if "Seed" in self.item_name:
            seed_ID = self.item_name.split('_')[0]
