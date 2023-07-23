import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilLayer:
    def __init__(self, all_sprites):
        # sprite groups
        self.all_sprites = all_sprites

        # 耕地的精灵组
        self.soil_sprites = pygame.sprite.Group()
        # 水地的精灵组
        self.water_sprites = pygame.sprite.Group()
        # graphics

        # 地图网格
        self.grid = None
        self.create_soil_grid()

        # 土壤的rect
        self.hit_rects = []
        self.create_hit_rects()


    def create_soil_grid(self):
        ground = pygame.image.load(r"asset/map.png")
        # 计算地图总共有多少个网格
        w_tiles, h_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        # 创建网格
        self.grid = [[[] for col in range(w_tiles)] for row in range(h_tiles)]

        tmx_data = load_pygame('asset/map.tmx')
        # 将可以耕种的图块加入网格
        for x, y, _ in tmx_data.get_layer_by_name('farmable').tiles():
            self.grid[y][x].append('F')

        # 将浅草地加入网格，在浅草地上的植物生长会较慢
        for x, y, _ in tmx_data.get_layer_by_name('light grass').tiles():
            self.grid[y][x].append('L')

        # 深草地上的植物生长快，保证区块与浅草地不重叠
        for x, y, _ in tmx_data.get_layer_by_name('deep grass').tiles():
            self.grid[y][x].append('D')

    def create_hit_rects(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def plough(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        # print(x, y)
        cell = self.grid[y][x]
        if 'F' in cell and 'X' not in cell:
            self.grid.append('X')
            self.grid[y][x].append(SoilTile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=pygame.image.load(r"asset\objects\outdoor_64_227.png"),
                groups=[self.all_sprites, self.soil_sprites],
            ))
        return self.grid[y][x]

    def water(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        if 'X' in cell and 'W' not in cell:
            self.grid[y][x].append('W')
            self.grid[y][x].append(WaterTile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=pygame.image.load(r"asset\objects\outdoor_64_682.png"),
                groups=[self.all_sprites, self.water_sprites]
            ))
        return self.grid[y][x]




class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']