import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from sprites.plants import Plant

class SoilLayer:
    def __init__(self, all_sprites, plant_group, collision_sprites):
        # sprite groups
        self.all_sprites = all_sprites
        # 植物的精灵组
        self.plant_group = plant_group
        # 碰撞的精灵组
        self.collision_sprites = collision_sprites


        # 耕地的精灵组
        self.soil_sprites = pygame.sprite.Group()
        # 湿地的精灵组
        self.water_sprites = pygame.sprite.Group()



        # 地图网格
        self.grid = None
        self.create_soil_grid()

        # 耕地音效
        self.plough_sound = pygame.mixer.Sound('asset/audio/锄地.mp3')
        # 浇水音效
        self.water_sound = pygame.mixer.Sound('asset/audio/浇水.mp3')



    def create_soil_grid(self):
        ground = pygame.image.load(r"asset/map.png").convert_alpha()
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


    def plough(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        self.plough_sound.play()
        cell = self.grid[y][x]
        if 'F' in cell and 'X' not in cell:
            self.grid[y][x].append('X')
            self.grid[y][x].append(SoilTile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=pygame.image.load(r"asset\objects\outdoor_64_227.png").convert_alpha(),
                groups=[self.all_sprites, self.soil_sprites]
            ))
        print('plough')


    def water(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        self.water_sound.play()
        if 'X' in cell and 'W' not in cell:
            self.grid[y][x].append('W')
            self.grid[y][x].append(WaterTile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=pygame.image.load(r"asset\objects\outdoor_64_682.png").convert_alpha(),
                groups=[self.all_sprites, self.water_sprites]
            ))
        print('water')

    def water_all(self):
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    self.grid[row_index][col_index].append('W')
                    self.grid[row_index][col_index].append(WaterTile(
                        pos=(col_index * TILE_SIZE, row_index * TILE_SIZE),
                        surf=pygame.image.load(r"asset\objects\outdoor_64_682.png").convert_alpha(),
                        groups=[self.all_sprites, self.water_sprites]
                    ))

    def plant(self, target_point, plant_type):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        if 'X' in cell and 'P' not in cell:
            # 创建plant
            self.grid[y][x].append('P')
            new_plant = Plant('fruittree', [self.plant_group, self.all_sprites, self.collision_sprites], (x * TILE_SIZE + 30, y * TILE_SIZE + 75))
            self.grid[y][x].append(new_plant)
            return True
        return False



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