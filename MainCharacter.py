import pygame


class MainCharacter:

    def __init__(self, map_width, map_height, screen):
        self.map_width = map_width
        self.map_height = map_height
        self.screen = screen

    animation = []
    map_width = 640
    map_height = 480
    width = 31
    height = 36
    posx = (map_width - width) / 2
    posy = (map_height - height) / 2

    direction = 0
    frame = 0
    animate = []

    def move_animate(self, direction):
        self.screen.fill((255, 255, 255))
        if not (direction == self.direction):
            self.frame = 0
            self.direction = direction
        self.screen.blit(self.animate[direction][self.frame], (self.posx, self.posy))
        self.frame = (self.frame + 1) % 3

    def move(self, dx, dy):
        self.posx += dx*(self.width/4)
        self.posy += dy*(self.height/4)
        if dx == 1:
            direction = 3
        if dx == -1:
            direction = 2
        if dy == 1:
            direction = 1
        if dy == -1:
            direction = 0
        self.move_animate(direction)

    def move_by_dire(self, direction):
        if direction == 0:
            self.move(0, -1)
        if direction == 1:
            self.move(0, 1)
        if direction == 2:
            self.move(-1, 0)
        if direction == 3:
            self.move(1, 0)

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