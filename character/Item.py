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
        self.description_whole = self.description_line.read()
        self.description = self.description_whole.split('_')[0]
        self.handled = False
        self.chosen = False
        self.num = 1

        self.cost = int(self.description_whole.split('_')[1])
        self.worth = int(self.description_whole.split('_')[2])


    def presentInBackPack(self, space):
        self.space = space
        self.posx = self.space.posx+6
        self.posy = self.space.posy
        self.icon = self.icon_backpack
        self.player = self.space.backpack.player
        self.screen = self.player.screen

    def display(self, isInventory):
        self.posx = self.space.posx + 6
        self.posy = self.space.posy
        if isInventory:
            self.screen.blit(self.icon_inventory, (self.posx, self.posy))
        else:
            self.screen.blit(self.icon_backpack, (self.posx, self.posy))
        if self.num > 1:
            font = pygame.font.Font('sources/UI/UIPack/Font/kenvector_future.ttf', 24)
            number = font.render(str(self.num), True, (0, 0, 0))
            if isInventory:
                self.screen.blit(number, (self.posx+50-20, self.posy+50-20))
            else:
                self.screen.blit(number, (self.posx+80-15, self.posy+80-25))

    def display_without_player(self, screen, isInventory, posx, posy):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        if isInventory:
            self.screen.blit(self.icon_inventory, (self.posx, self.posy))
        else:
            self.screen.blit(self.icon_backpack, (self.posx, self.posy))
        if self.num > 1:
            font = pygame.font.Font('sources/UI/UIPack/Font/kenvector_future.ttf', 24)
            number = font.render(str(self.num), True, (0, 0, 0))
            if isInventory:
                self.screen.blit(number, (self.posx + 50 - 20, self.posy + 50 - 20))
            else:
                self.screen.blit(number, (self.posx + 80 - 15, self.posy + 80 - 25))

    def decrease(self):
        self.num -= 1
        if self.num <= 0:
            self.space.item = None
            temp = self.player.equiped_num
            self.player.equipItem(self.player.equiped_num)
            self.player.equipItem(temp)
            self.space.occupied = False

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
                tree_death = False
                for i in self.player.tree_group:
                    if i.rect.collidepoint(self.player.interaction_point):
                        tree_death = i.damage()
                #for i in self.player
                self.player.useItemAnimate(self.item_name)
                if tree_death:
                    self.player.gainItem(Item("Wood"))
                    self.player.gainItem(Item("Seed_fruittree"))

        if "Seed" in self.item_name:
            seed_type = self.item_name.split('_')[1]
            if "tree" in self.item_name:
                plant = self.player.map_grid.plant_tree(interaction_point, seed_type)
            else:
                plant = self.player.map_grid.plant_crop(interaction_point, seed_type)
            if plant:
                self.decrease()
