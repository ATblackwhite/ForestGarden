import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from sprites.plants import Plant, Crop, update_harvestable, Bling

class SoilLayer:
    def __init__(self, all_sprites, plant_group, collision_sprites, bling_groups, game):
        # sprite groups
        self.all_sprites = all_sprites
        # 植物的精灵组
        self.plant_group = plant_group
        # 碰撞的精灵组
        self.collision_sprites = collision_sprites
        # bling的精灵组
        self.bling_groups = bling_groups

        self.game = game

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
        # print('plough')


    def water(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        self.water_sound.play()
        cell = self.grid[y][x]
        if 'X' in cell:
            for item in self.grid[y][x]:
                if isinstance(item, Plant):
                    bling = Bling(item.rect.midbottom + pygame.Vector2(50, 200), [self.bling_groups, self.all_sprites],
                                  'blue')
                    item.stagevideo.append(bling)
                    item.water = 1.1
                    item.relationship += 1
            if 'W' not in cell:
                self.grid[y][x].append('W')
                self.grid[y][x].append(WaterTile(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=pygame.image.load(r"asset\objects\outdoor_64_682.png").convert_alpha(),
                    groups=[self.all_sprites, self.water_sprites],
                    soil_layer=self
                ))
        # print('water')

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

    def plant_tree(self, target_point, plant_type):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        # 土壤被开垦且没有种植
        if 'X' in cell and 'P' not in cell:
            # 创建plant
            self.grid[y][x].append('P')
            tree = Plant(f'{plant_type}', [self.plant_group, self.all_sprites, self.collision_sprites], (x * TILE_SIZE, y * TILE_SIZE))
            self.grid[y][x].append(tree)
            return True
        return False

    def plant_crop(self, target_point, plant_type):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        # 土壤被开垦且没有种植
        if 'X' in cell and 'P' not in cell:
            # 创建crop
            self.grid[y][x].append('P')
            new_plant = Crop(f'{plant_type}', [self.plant_group, self.all_sprites, self.collision_sprites], (x * TILE_SIZE, y * TILE_SIZE))
            self.grid[y][x].append(new_plant)
            return True
        return False

    def harvest(self, target_point):
        x = int(target_point.x // TILE_SIZE)
        y = int(target_point.y // TILE_SIZE)
        cell = self.grid[y][x]
        print('收获')
        if 'P' in cell:
            for item in self.grid[y][x]:
                # 确认这个网格上种植了Crop
                if isinstance(item, Crop):
                    crop = item
                    return update_harvestable(crop, self.all_sprites)
        # 返回None说明这个格子上并没有种植作物
        return None

    def talk(self, target_point):
        self.game.handle_mouse_click_talk(target_point)



class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']




class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, soil_layer):
        super().__init__(groups)
        self.pos = pos
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']
        self.start_time = pygame.time.get_ticks()
        self.soil_layer = soil_layer

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 5000:
            x, y = self.pos
            x = x // TILE_SIZE
            y = y // TILE_SIZE
            self.soil_layer.grid[y][x].remove(self)
            self.soil_layer.grid[y][x].remove('W')
            for item in self.soil_layer.grid[y][x]:
                if isinstance(item, Plant):
                    item.water = 1
            self.kill()