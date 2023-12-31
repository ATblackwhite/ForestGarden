import pygame
from character.TextWrapTool import displayText
from sprites.generic import *
from sprites.tree import *
from settings import *
from camera.cameraGroup import *
from character.Item import *


class MainCharacter(pygame.sprite.Sprite):
    width = 31
    height = 36

    movement = []
    # New
    direct_move = {
        0: (0, -1),
        1: (0, 1),
        2: (-1, 0),
        3: (1, 0)
    }
    direction = 0
    move_frame = 0
    ani_frame = 0
    animate = []
    item_ani = {}

    item_animating = False
    item_frame_animating = False
    moving = False
    gainItemAnimating = False

    equiped_num = -1
    equiped_item = None
    new_item = None

    trader_met = False
    text_bar_show = False

    gold = 100

    def __init__(self, map_width, map_height, screen, pos, group, collision_group, soil_layer, tree_sprite, trader):

        super().__init__(group)
        self.collision_group = collision_group
        self.tree_group = tree_sprite
        self.map_grid = soil_layer
        self.trader = trader

        self.map_width = map_width
        self.map_height = map_height
        self.screen = screen
        self.loadAnimation()
        self.ownBackpack(Backpack(self))
        self.ownInventory(Inventory(self))
        self.ownShop(Shop(self))
        self.pos = pos
        self.posx, self.posy = pos
        # New
        self.interaction_point_x = self.posx + self.width / 2 + self.direct_move[self.direction][0] * self.width * 2
        self.interaction_point_y = self.posy + self.height / 2 + self.direct_move[self.direction][1] * self.height * 2

        # New
        if self.item_animating:
            status = self.equiped_item.item_name + str(self.direction)
            self.image = self.item_ani[status][self.ani_frame]
        else:
            self.image = self.animate[self.direction][self.move_frame]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.75)
        self.rect = self.image.get_rect(center=pos)

    def update_to_camera(self):
        if self.item_animating:
            status = self.equiped_item.item_name
            self.image = self.item_ani[status][self.direction][self.ani_frame]
            self.useItemAnimate(self.equiped_item.item_name)
        else:
            self.image = self.animate[self.direction][self.move_frame]
        self.pos = pygame.math.Vector2(self.posx, self.posy)
        self.rect = self.image.get_rect(center=self.pos)
        self.z = LAYERS['main']

    # 行走动画
    def move_animate(self, direction, duration=150):
        current_time = pygame.time.get_ticks()
        if not (direction == self.direction):
            self.move_frame = 0
            self.direction = direction
        if (current_time - self.animate_start_time) >= duration:
            self.move_frame += 1
            self.move_frame = self.move_frame % len(self.animate[self.direction])
            self.moving = False

    # 坐标变化
    def move(self, dx, dy):
        self.pos = pygame.math.Vector2(self.posx, self.posy)
        # 水平移动
        self.posx += dx * (self.width / 4)
        self.hitbox.centerx = self.posx

        # 垂直移动
        self.posy += dy * (self.height / 4)
        self.hitbox.centery = self.posy
        self.pos = pygame.math.Vector2(self.posx, self.posy)
        self.rect.center = self.hitbox.center
        for sprite in self.collision_group:
            if sprite.hitbox.colliderect(self.hitbox):
                self.posx -= dx * (self.width / 4)
                self.posy -= dy * (self.height / 4)
                self.pos = pygame.math.Vector2(self.posx, self.posy)
                self.hitbox.centerx = round(self.posx)
                self.hitbox.centery = round(self.posy)
                self.rect.center = self.hitbox.center

        if dx == 1:
            self.direction = 3
        if dx == -1:
            self.direction = 2
        if dy == 1:
            self.direction = 1
        if dy == -1:
            self.direction = 0

        if not self.moving:
            self.moving = True
            self.animate_start_time = pygame.time.get_ticks()
        self.move_animate(self.direction, 150)

    # 坐标变化（另一种输入）
    def move_by_dire(self, direction):
        if direction == 0:
            self.move(0, -1)
        if direction == 1:
            self.move(0, 1)
        if direction == 2:
            self.move(-1, 0)
        if direction == 3:
            self.move(1, 0)

    def ownBackpack(self, backpack):
        self.backpack = backpack
        self.backpack.createSpace()

    def ownInventory(self, inventory):
        self.inventory = inventory
        self.inventory.createHandSpace()

    def openBackpack(self):
        self.backpack.space_list[self.backpack.choosed_x][self.backpack.choosed_y].choosed = True
        self.backpack.display()

    def ownShop(self, shop):
        self.shop = shop
        self.shop.createBuy()
        self.shop.createSell()

    def openShop(self):
        if self.shop.state:
            self.shop.sell_list[self.shop.choosed_x][self.shop.choosed_y].choosed = True
        else:
            self.shop.buy_list[self.shop.choosed_x].choosed = True
        self.shop.display()

    def gainItem(self, item):
        space_left = False
        for i in self.backpack.space_list:
            for j in i:
                if j.item != None and j.item.item_name == item.item_name:
                    j.addItem(item.num)
                    space_left = True
                    break

        for i in self.inventory.hand_list:
            if i.item != None and i.item.item_name == item.item_name:
                i.addItem(item.num)
                space_left = True
                break

        if not space_left:
            for i in self.backpack.space_list:
                for j in i:
                    if not j.occupied:
                        j.pushItem(item)
                        space_left = True
                        break
                if space_left:
                    break

        if space_left:
            self.new_item = item
            self.gainItemAnimating = True
            self.notice_start_time = pygame.time.get_ticks()

        else:
            print("NO Space left")

    def equipItem(self, equip_num):
        if equip_num in range(5):
            self.inventory.moveChose(equip_num)
            if equip_num != self.equiped_num:
                self.equiped_num = equip_num
                self.equiped_item = self.inventory.hand_list[self.equiped_num].item
            else:
                self.equiped_num = -1
                self.equiped_item = None

    def noticeGain(self, duration=1000, num=1):
        self.gainItemAnimating = True

        current_time = pygame.time.get_ticks()
        font = pygame.font.Font(size=48)
        number = font.render(str('x' + str(num)), True, (0, 0, 0))

        self.screen.blit(self.new_item.icon_backpack,
                         ((SCREEN_WIDTH - self.width) / 2 - 50, (SCREEN_HEIGHT - self.height) / 2 - 100))
        self.screen.blit(number, ((SCREEN_WIDTH - self.width) / 2 + 30, (SCREEN_HEIGHT - self.height) / 2 - 50))

        if (current_time - self.notice_start_time) >= duration:
            self.gainItemAnimating = False

    # New
    def interaction(self):
        self.interaction_point_x = self.hitbox.centerx+ self.direct_move[self.direction][0] * self.width * 2
        self.interaction_point_y = self.hitbox.centery + self.direct_move[self.direction][1] * self.height * 2
        self.interaction_point = pygame.math.Vector2(self.interaction_point_x, self.interaction_point_y)
        if self.equiped_item != None:
            self.equiped_item.item_use(self.interaction_point)
        else:
            if self.trader.rect.collidepoint(self.interaction_point):
                if self.trader_met:
                    self.openShop()
                else:
                    self.trader_met = True
                    self.text_bar_show = True
            harvest = self.backpack.player.map_grid.harvest(self.interaction_point)
            if harvest != None:
                seed_name = "Fruit_" + harvest
                self.backpack.player.gainItem(Item(seed_name))

    def talkToPlants(self):
        self.interaction_point_x = self.hitbox.centerx + self.direct_move[self.direction][0] * self.width * 2
        self.interaction_point_y = self.hitbox.centery + self.direct_move[self.direction][1] * self.height * 2
        self.interaction_point = pygame.math.Vector2(self.interaction_point_x, self.interaction_point_y)
        self.map_grid.talk(self.interaction_point)

    def useItemAnimate(self, item_name, duration=200):
        self.item_animating = True

        if not self.item_frame_animating:
            self.item_frame_animating = True
            self.animate_start_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()

        if (current_time - self.animate_start_time) >= duration:
            self.item_frame_animating = False
            self.ani_frame += 1

        item_ani_group = self.item_ani[item_name]
        if self.ani_frame == len(item_ani_group[self.direction]):
            self.item_animating = False
            self.ani_frame = 0

    def goldShow(self):
        background = pygame.transform.scale(pygame.image.load('sources/UI/UIPack/PNG/yellow_button13.png'), (200, 60))
        gold_img = pygame.transform.scale(pygame.image.load('sources/Item/Gold/Icon32.png'), (45, 45))
        font = pygame.font.Font(size=48)
        text = font.render(str(self.gold), True, (0, 0, 0))
        self.screen.blit(background, (1370, 30))
        self.screen.blit(gold_img, (1390, 35))
        self.screen.blit(text, (1450, 42))


    # 前置加载
    def loadAnimation(self):
        # 行走动画

        for i in range(4):
            self.animate.append([])
            for j in range(4):
                if i * 4 + j + 1 < 10:
                    route = 'sources/Character/CatCharacter/Walk/Basic Charakter Spritesheet_00' + str(
                        i * 4 + j + 1) + '.png'
                else:
                    route = 'sources/Character/CatCharacter/Walk/Basic Charakter Spritesheet_0' + str(
                        i * 4 + j + 1) + '.png'
                self.animate[i].append(pygame.transform.scale(pygame.image.load(route), (200, 200)))

        # 道具使用动画
        # Pot
        self.item_ani["Pot"] = []
        for i in range(4):
            self.item_ani["Pot"].append([])
            for j in range(2):
                route = 'sources/Character/CatCharacter/Item_Use/Basic Charakter Actions_0' + str(
                    i * 2 + j + 1 + 16) + '.png'
                self.item_ani["Pot"][i].append(pygame.transform.scale(pygame.image.load(route), (200, 200)))

        # Axe
        self.item_ani["Axe"] = []
        for i in range(4):
            self.item_ani["Axe"].append([])
            for j in range(2):
                if i * 2 + j + 1 + 8 < 10:
                    route = 'sources/Character/CatCharacter/Item_Use/Basic Charakter Actions_00' + str(
                        i * 2 + j + 1 + 8) + '.png'
                else:
                    route = 'sources/Character/CatCharacter/Item_Use/Basic Charakter Actions_0' + str(
                        i * 2 + j + 1 + 8) + '.png'
                self.item_ani["Axe"][i].append(pygame.transform.scale(pygame.image.load(route), (200, 200)))

        # Hoe
        self.item_ani["Hoe"] = []
        for i in range(4):
            self.item_ani["Hoe"].append([])
            for j in range(2):
                route = 'sources/Character/CatCharacter/Item_Use/Basic Charakter Actions_00' + str(
                    i * 2 + j + 1) + '.png'
                self.item_ani["Hoe"][i].append(pygame.transform.scale(pygame.image.load(route), (200, 200)))


class Backpack:
    posx = 200
    posy = 100
    backpack_backgroung = pygame.image.load('sources/UI/UIPack/PNG/yellow_button05.png')
    backpack_background = pygame.transform.scale(backpack_backgroung, (1200, 600))
    space_list = []
    space_row = 4
    space_column = 5
    opened = False

    # used in main
    item_chose = None
    item_switch = None

    choosed_x = 0
    choosed_y = 0

    def __init__(self, player):
        self.player = player

    def createSpace(self):
        for i in range(self.space_row):
            self.space_list.append([])
            for j in range(self.space_column):
                self.space_list[i].append(BackSpace(j, i, self))
        self.space_list[self.choosed_x][self.choosed_y].choosed = True

    def showDetail(self, item):
        if item != None:
            show_img = pygame.transform.scale(item.icon, (200, 200))
            self.player.screen.blit(show_img, (720 + self.space_list[0][0].posx, self.space_list[0][0].posy))
            displayText(item.description, self.player.screen, 60, 720 + self.space_list[0][0].posx, 60 + self.space_list[0][0].posy + 200)

    def display(self):
        self.opened = True
        self.player.screen.blit(self.backpack_background, (self.posx, self.posy))
        for i in self.space_list:
            for j in i:
                j.display()

    def closeBackpack(self):
        self.space_list[self.choosed_x][self.choosed_y].choosed = False
        self.choosed_x = 0
        self.choosed_y = 0
        self.opened = False

    def moveChose(self, dy, dx):
        if (0 <= (self.choosed_x + dx) < 4) and (0 <= (self.choosed_y + dy) < 5):
            self.space_list[self.choosed_x][self.choosed_y].choosed = False
            self.choosed_x += dx
            self.choosed_y += dy
            self.space_list[self.choosed_x][self.choosed_y].choosed = True

    def moveWithMouse(self, item, mouse_x, mouse_y):
        if item != None:
            moving_img = item.icon
            self.player.screen.blit(moving_img, (mouse_x, mouse_y))

    def checkMouseChose(self, mouse_pos):
        for i in self.space_list:
            for j in i:
                if j.ifMouseChose(mouse_pos[0], mouse_pos[1]):
                    return j
        for i in self.player.inventory.hand_list:
            if i.ifMouseChose(mouse_pos[0], mouse_pos[1]):
                return i

    def switchItem(self, desti_space, item1=None, item2=None):
        if item1 == None or desti_space == None:
            return
        elif item2 == None:
            temp_space = item1.space
            desti_space.pushItem(item1)
            temp_space.item = None
            temp_space.occupied = False
        elif item1.item_name == item2.item_name and desti_space != item1.space:
            item2.num += item1.num
            item1.space.item = None
            item1.space.occupied = False
        else:
            temp_space = item1.space
            item2.space.pushItem(item1)
            temp_space.pushItem(item2)
        self.display()
        temp = self.player.equiped_num
        self.player.equipItem(self.player.equiped_num)
        self.player.equipItem(temp)


class BackSpace:
    width = 98
    height = 98

    def __init__(self, x, y, backpack):
        self.backpack = backpack
        self.occupied = False
        self.normal_img = pygame.image.load('sources/UI/UIPack/PNG/yellow_button06.png')
        self.normal_img = pygame.transform.scale(self.normal_img, (self.width, self.height))
        self.chosen_img = pygame.image.load('sources/UI/UIPack/PNG/red_button03.png')
        self.chosen_img = pygame.transform.scale(self.chosen_img, (self.width, self.height))
        self.x = x
        self.y = y
        self.posx = (40 * x + self.width * x) + (backpack.posx + 40)
        self.posy = (40 * y + self.height * y) + (backpack.posy + 40)
        self.item = None
        self.choosed = False

    def pushItem(self, item):
        self.item = item
        item.presentInBackPack(self)
        self.occupied = True

    def addItem(self, num=1):
        self.item.num += num

    def display(self):
        if self.choosed:
            self.backpack.showDetail(self.item)
            self.backpack.player.screen.blit(self.chosen_img, (self.posx, self.posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (self.posx, self.posy))
        if self.item != None:
            self.item.display(0)

    def display_by_position(self, posx, posy):
        pre_posx = self.posx
        pre_posy = self.posy
        self.posx = posx
        self.posy = posy
        if self.choosed:
            self.backpack.player.shop.showDetail(self.item)
            self.backpack.player.screen.blit(self.chosen_img, (posx, posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (posx, posy))
        if self.item != None:
            self.item.display(0)

        self.posx = pre_posx
        self.posy = pre_posy

    def ifMouseChose(self, mouse_x, mouse_y):
        if self.posx <= mouse_x < self.posx + self.width and self.posy <= mouse_y <= self.posy + self.height:
            return True
        else:
            return False


class Inventory(Backpack):
    posx = 600
    posy = 770
    hand_background = pygame.image.load('sources/UI/UIPack/PNG/green_button13.png')
    hand_background = pygame.transform.scale(hand_background, (400, 100))
    hand_list = []
    hand_capacity = 5
    chosen_ID = -1

    def createHandSpace(self):
        for i in range(self.hand_capacity):
            self.hand_list.append(HandSpace(i, 0, self))

    def display(self):
        self.player.screen.blit(self.hand_background, (self.posx, self.posy))
        for i in self.hand_list:
            i.display()

    def moveChose(self, desti):
        if desti == self.chosen_ID:
            self.hand_list[self.chosen_ID].choosed = False
            self.chosen_ID = -1
        else:
            self.hand_list[self.chosen_ID].choosed = False
            self.chosen_ID = desti
            self.hand_list[self.chosen_ID].choosed = True


class HandSpace(BackSpace):
    width = 60
    height = 60

    def __init__(self, x, y, inventory):
        super(HandSpace, self).__init__(x, y, inventory)
        self.inventory = inventory
        self.posx = self.inventory.posx + 30 + (10 + self.width) * x
        self.posy = self.inventory.posy + 15

    def pushItem(self, item):
        self.item = item
        item.presentInBackPack(self)
        self.occupied = True

    def display(self):
        if self.choosed:
            self.backpack.player.screen.blit(self.chosen_img, (self.posx, self.posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (self.posx, self.posy))
        if self.item != None:
            self.item.display(1)


#Shop
class Shop(Backpack):
    def __init__(self, player):
        self.player = player
        self.buy_button = ShopButton(self.posx + self.width+50, self.posy + 100, "Buy", self)
        self.sell_button = ShopButton(self.posx + self.width+50, self.posy + 400, "Sell", self)

    width = 1300
    height = 700
    background = pygame.image.load('sources/UI/UIPack/PNG/grey_button02.png')
    backpack_background = pygame.transform.scale(background, (width, height))
    state = 0
    posy = 20
    posx = 50

    buy_list = []
    item_for_sell = ["Axe", "Pot", "Hoe", "Seed_tomato", "Seed_corn", "Seed_fruittree", "Fruit_tomato", "Fruit_corn"]
    sell_list = []

    list_head = 0
    list_tail = 5

    def createBuy(self):
        for i in range(6):
            self.buy_list.append(BuySpace(i, 0, self))
            self.buy_list[i].item = Item(self.item_for_sell[i])
        self.buy_list[0].choosed = True

    def createSell(self):
        for i in range(self.space_row):
            self.sell_list.append([])
            for j in range(self.space_column):
                self.sell_list[i].append(self.player.backpack.space_list[i][j])
        self.sell_list[0][0].choosed = True

    def display(self):
        self.opened = True
        self.player.screen.blit(self.backpack_background, (self.posx, self.posy))
        if self.state:
            for i in self.sell_list:
                for j in i:
                    j.display_by_position(j.posx-90, j.posy-30)
        else:
            for i in self.buy_list:
                i.display()

        self.buy_button.display()
        self.sell_button.display()

    def closeShop(self):
        if self.state:
            self.sell_list[self.choosed_x][self.choosed_y].choosed = False
        else:
            self.buy_list[self.choosed_x].choosed = False
        self.choosed_x = 0
        self.choosed_y = 0
        self.opened = False

    def moveChose(self, dy, dx):
        if self.state:
            if (0 <= (self.choosed_x + dx) < 4) and (0 <= (self.choosed_y + dy) < 5):
                self.sell_list[self.choosed_x][self.choosed_y].choosed = False
                self.choosed_x += dx
                self.choosed_y += dy
                self.sell_list[self.choosed_x][self.choosed_y].choosed = True
        else:
            if 0 <= (self.choosed_x + dx) < len(self.buy_list):
                self.buy_list[self.choosed_x].choosed = False
                self.choosed_x += dx
                self.buy_list[self.choosed_x].choosed = True
            elif (self.choosed_x+dx)<self.list_head and self.list_head-1 >= 0:
                self.list_head-=1
                self.list_tail-=1
            elif 5<(self.choosed_x+dx) and self.list_tail+1 < len(self.item_for_sell):
                self.list_head+=1
                self.list_tail+=1
            for i in range(6):
                self.buy_list[i].item = Item(self.item_for_sell[i+self.list_head])


    def buy(self):
        if self.player.gold >= self.buy_list[self.choosed_x].item.cost:
            self.player.gold -= self.buy_list[self.choosed_x].item.cost
            self.player.gainItem(Item(self.buy_list[self.choosed_x].item.item_name))
        else:
            print("No enough gold")

    def sell(self):
        if self.sell_list[self.choosed_x][self.choosed_y].item != None:
            self.player.gold += self.sell_list[self.choosed_x][self.choosed_y].item.worth
            self.sell_list[self.choosed_x][self.choosed_y].item.decrease()

    def showDetail(self, item):
        if item != None:
            show_img = pygame.transform.scale(item.icon, (200, 200))

            if self.state:
                self.player.screen.blit(show_img, (780 + self.posx, 40 + self.posy))
                displayText(item.description, self.player.screen, 60, 780 + self.posx, 60 + self.posy + 200)
                evaluate = "Worth:" + str(item.worth)
                displayText(evaluate, self.player.screen, 60, 780 + self.posx, self.posy + 600 - 60)
            else:
                self.player.screen.blit(show_img, (720 + self.posx, 40 + self.posy))
                displayText(item.description, self.player.screen, 60, 720 + self.posx, 60 + self.posy + 200)
                evaluate = "Cost:" + str(item.cost)
                displayText(evaluate, self.player.screen, 60, 720 + self.posx, self.posy+600-60)



class BuySpace(BackSpace):
    def __init__(self, x, y, shop):
        super(BuySpace, self).__init__(x, y, shop)
        self.width = 450
        self.height = 80
        self.posx = self.backpack.posx+100
        self.posy = (self.height+20)*x + 70
        self.normal_img = pygame.transform.scale(pygame.image.load('sources/UI/UIPack/PNG/grey_button14.png'), (self.width, self.height))
        self.chosen_img = pygame.transform.scale(pygame.image.load('sources/UI/UIPack/PNG/red_button10.png'), (self.width, self.height))

    def display(self):
        if self.choosed:
            self.backpack.showDetail(self.item)
            self.backpack.player.screen.blit(self.chosen_img, (self.posx, self.posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (self.posx, self.posy))
        if self.item != None:
            self.item.display_without_player(self.backpack.player.screen, 0, self.posx+20, self.posy-20)
            displayText(self.item.item_name, self.backpack.player.screen, 60, self.posx + 120, self.posy+40)



class ShopButton:
    def __init__(self, posx, posy, text, shop):
        self.posx = posx
        self.posy = posy
        self.shop = shop
        self.height = 80
        self.width = 100
        self.text = text[:]
        self.background_unchosen = pygame.transform.scale(pygame.image.load('sources/UI/UIPack/PNG/grey_button08.png'), (self.width,self.height))
        self.background_chosen = pygame.transform.scale(pygame.image.load('sources/UI/UIPack/PNG/grey_button09.png'), (self.width, self.height))
        if self.text == "Buy":
            self.chosen = True
        else:
            self.chosen = False

    def checkClick(self, mouseposx, mouseposy):
        if self.posx<=mouseposx<=self.posx+self.width and self.posy <= mouseposy <= self.posy+self.height:
            self.click()

    def click(self):
        prev_state = self.shop.state
        if self.text == "Buy":
            self.shop.state = 0
            self.shop.sell_button.chosen = False
            self.shop.buy_button.chosen = True
        elif self.text == "Sell":
            self.shop.state = 1
            self.shop.buy_button.chosen = False
            self.shop.sell_button.chosen = True
        if prev_state != self.shop.state:
            if prev_state == 0:
                self.shop.buy_list[self.shop.choosed_x].choosed = False
            else:
                self.shop.sell_list[self.shop.choosed_x][self.shop.choosed_y].choosed = False
            self.shop.choosed_x = 0
            self.shop.choosed_y = 0
            self.shop.moveChose(0, 0)

    def display(self):
        if self.chosen:
            self.shop.player.screen.blit(self.background_chosen, (self.posx, self.posy))
        else:
            self.shop.player.screen.blit(self.background_unchosen, (self.posx, self.posy))
        displayText(self.text, self.shop.player.screen, 60, self.posx+20, self.posy+20, size=48, Font="")
