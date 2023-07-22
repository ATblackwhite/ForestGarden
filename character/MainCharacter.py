import pygame
from character.TextWrapTool import displayText
from sprites.generic import *
from sprites.tree import *
from settings import *
from camera.cameraGroup import *

class MainCharacter(pygame.sprite.Sprite):

    animation = []
    width = 31
    height = 36


    movement = []
    direction = 0
    move_frame = 0
    ani_frame = 0
    animate = []
    item_ani = {}

    item_animating = False

    equiped_num = -1
    equiped_item = None

    #New
    def __init__(self, map_width, map_height, screen, pos, group):
        super().__init__(group)

        self.map_width = map_width
        self.map_height = map_height
        self.screen = screen
        self.loadAnimation()
        self.ownBackpack(Backpack(self))
        self.ownInventory(Inventory(self))
        self.loadAnimation()
        self.pos = pos
        self.posx, self.posy = pos

        #New
        if self.item_animating:
            status = self.equiped_item.item_id + str(self.direction)
            self.image = self.item_ani[self.status][self.ani_frame]
        else:
            self.image = self.animate[self.direction][self.move_frame]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']


    def update_to_camera(self):
        if self.item_animating:
            status = self.equiped_item.item_id + str(self.direction)
            self.image = self.item_ani[self.status][self.ani_frame]
        else:
            self.image = self.animate[self.direction][self.move_frame]
        self.pos = self.offset = pygame.math.Vector2(self.posx, self.posy)
        self.rect = self.image.get_rect(center=self.pos)
        self.z = LAYERS['main']

    # 行走动画
    def move_animate(self, direction):
        if not (direction == self.direction):
            self.move_frame = 0
            self.direction = direction
        self.move_frame += 1
        self.move_frame = self.move_frame% 3

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

    def equipItem(self, equip_num):
        self.inventory.moveChose(equip_num)
        if equip_num != self.equiped_num:
            self.equiped_num = equip_num
            self.equiped_item = self.inventory.hand_list[self.equiped_num].item
        else:
            self.equiped_num = -1
            self.equiped_item = None

    def useItemAnimate(self, item_ID):
        self.item_animating = True
        item_ani_group = self.item_ani[item_ID]
        display_frame = item_ani_group[self.direction][self.ani_frame]
        self.ani_frame += 1
        if self.ani_frame == len(item_ani_group[self.direction]):
            self.item_animating = False
        return display_frame


    # 前置加载
    def loadAnimation(self):
        # 行走动画
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

        # 道具使用动画


class Backpack:
    posx = 41.5
    posy = 20
    backpack_backgroung = pygame.image.load('sources/UI/UIPack/PNG/yellow_button05.png')
    backpack_background = pygame.transform.scale(backpack_backgroung, (600, 300))
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
        item.presentInBackPack(self, True)
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
        if self.posx <= mouse_x < self.posx + self.width and self.posy <= mouse_y <= self.posy + self.height:
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
    width = 30
    height = 30

    def __init__(self, x, y, inventory):
        super(HandSpace, self).__init__(x, y, inventory)
        self.inventory = inventory
        self.posx = self.inventory.posx + 15 + (5 + self.width) * x
        self.posy = self.inventory.posy + 7.5

    def pushItem(self, item):
        self.item = item
        item.presentInBackPack(self, False)
        self.occupied = True

    def display(self):
        if self.choosed:
            self.backpack.player.screen.blit(self.chosen_img, (self.posx, self.posy))
        else:
            self.backpack.player.screen.blit(self.normal_img, (self.posx, self.posy))
        if self.item != None:
            self.item.display()
