import pygame
from character.TextWrapTool import displayText


class MainCharacter:

    def __init__(self, map_width, map_height, screen):
        self.map_width = map_width
        self.map_height = map_height
        self.screen = screen
        self.loadAnimation()

    animation = []
    map_width = 640
    map_height = 480
    width = 31
    height = 36
    posx = (map_width - width) / 2
    posy = (map_height - height) / 2

    movement = []
    direction = 0
    frame = 0
    animate = []

    equiped_num = 0
    equiped_item = None

    # 行走动画
    def move_animate(self, direction):
        if not (direction == self.direction):
            self.frame = 0
            self.direction = direction

    def display(self, frameChange):
        self.screen.blit(self.animate[self.direction][self.frame], (self.posx, self.posy))
        self.frame = (self.frame + frameChange) % 3


    # 坐标变化
    def move(self, dx, dy):
        self.posx += dx * (self.width / 4)
        self.posy += dy * (self.height / 4)
        if dx == 1:
            self.direction = 3
        if dx == -1:
            self.direction = 2
        if dy == 1:
            self.direction = 1
        if dy == -1:
            self.direction = 0
        self.move_animate(self.direction)

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

    # 前置加载
    def loadAnimation(self):

        front = []
        back = []
        left = []
        right = []

        f1 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_008.png')
        f2 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_007.png')
        f3 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_009.png')

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_011.png')
        r2 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_010.png')
        r3 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_012.png')

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_002.png')
        b2 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_001.png')
        b3 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_003.png')

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_005.png')
        l2 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_004.png')
        l3 = pygame.image.load('sources/Character/rpgsprites1/seperateImage/warrior_m_006.png')

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animate.append(back)
        self.animate.append(front)
        self.animate.append(right)
        self.animate.append(left)

    def ownBackpack(self, backpack):
        self.backpack = backpack
        self.backpack.createSpace()

    def ownInventory(self, inventory):
        self.inventory = inventory
        self.inventory.createHandSpace()

    def openBackpack(self):
        self.backpack.display()

    def gainItem(self, item):
        space_left = False
        for i in self.backpack.space_list:
            for j in i:
                if not j.occupied:
                    j.pushItem(item)
                    space_left = True
                    break
            if space_left:
                break
        if not space_left:
            print("NO Space left")

#    def equipItem(self, item):


class Backpack:
    posx = 41.5
    posy = 20
    backpack_backgroung = pygame.image.load('sources/UI/UIPack/PNG/yellow_button05.png')
    backpack_background = pygame.transform.scale(backpack_backgroung, (600, 300))
    space_list = []
    space_row = 4
    space_column = 5
    opened = False

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
            show_img = pygame.transform.scale(item.icon, (100, 100))
            self.player.screen.blit(show_img, (360 + self.posx, 20 + self.posy))
            displayText(item.description, self.player.screen, 30, 370 + self.posx, 20 + self.posy + 100)

    def display(self):
        self.opened = True
        self.player.screen.blit(self.backpack_background, (self.posx, self.posy))
        for i in self.space_list:
            for j in i:
                j.display()

    def close(self):
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

    def switchItem(self, desti_space, item1=None, item2=None):
        if item1 == None or desti_space == None:
            return
        if item2 == None:
            temp_space = item1.space
            desti_space.pushItem(item1)
            temp_space.item = None
            temp_space.occupied = False
        else:
            temp_space = item1.space
            item2.space.pushItem(item1)
            temp_space.pushItem(item2)
        self.display()


class BackSpace:

    width = 49
    height = 49

    def __init__(self, x, y, backpack):
        self.backpack = backpack
        self.occupied = False
        self.normal_img = pygame.image.load('sources/UI/UIPack/PNG/yellow_button06.png')
        self.normal_img = pygame.transform.scale(self.normal_img, (self.width, self.height))
        self.chosen_img = pygame.image.load('sources/UI/UIPack/PNG/red_button03.png')
        self.chosen_img = pygame.transform.scale(self.chosen_img, (self.width, self.height))
        self.x = x
        self.y = y
        self.posx = (20 * x + self.width * x) + (backpack.posx + 20)
        self.posy = (20 * y + self.height * y) + (backpack.posy + 20)
        self.item = None
        self.choosed = False

    def pushItem(self, item):
        self.item = item
        item.presentInBackPack(self)
        self.occupied = True

    def display(self):
        if self.choosed:
            self.backpack.showDetail(self.item)
            self.backpack.player.screen.blit(self.chosen_img, (self.posx, self.posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (self.posx, self.posy))
        if self.item != None:
            self.item.display()

    def ifMouseChose(self, mouse_x, mouse_y):
        if self.posx <= mouse_x < self.posx + self.width and self.posy <= mouse_y <= self.posy+self.height:
            return True
        else:
            return False


class Inventory(Backpack):
    posx = 240
    posy = 320
    hand_background = pygame.image.load('sources/UI/UIPack/PNG/green_button13.png')
    hand_background = pygame.transform.scale(hand_background, (200, 50))
    hand_list = []
    hand_capacity = 5
    chosen_ID = 0

    def createHandSpace(self):
        for i in range(self.hand_capacity):
            self.hand_list.append(HandSpace(i, 0, self))

    def display(self):
        self.player.screen.blit(self.hand_background, (self.posx, self.posy))
        for i in self.hand_list:
            i.display()


class HandSpace(BackSpace):

    width = 30
    height = 30

    def __init__(self, x, y, inventory):
        super(HandSpace, self).__init__(x, y, inventory)
        self.inventory = inventory
        self.posx = self.inventory.posx+15+(5+self.width)*x
        self.posy = self.inventory.posy+7.5

