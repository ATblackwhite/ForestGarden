import pygame.sprite

import re  # 添加这一行导入语句
from UI.interface.mainMenu import MainMenu
from character.MainCharacter import *
from character.Item import *
from settings import *
from camera.cameraGroup import CameraGroup
from sprites.generic import Generic
from sprites.tree import Tree
from sprites.map import Map
from pytmx.util_pygame import load_pygame
from camera.soilLayer import SoilLayer

from sprites.plants import Plant, Emotes,Crop,Bling,Talk

from UI.rain import Rain
from UI.interface.textBar import TextBar


movement = []
need_moveWithMouse = False
# plant_group = pygame.sprite.Group()
# emotes_group = pygame.sprite.Group()

class ForestGarden:
    # 管理游戏的类
    def __init__(self):
        # 初始化游戏
        pygame.init()
        # 设置屏幕大小
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 设置游戏标题
        pygame.display.set_caption("Forest Garden")
        # 载入游戏主界面
        self.main_menu = MainMenu(self)
        # 添加系统时钟
        self.clock = pygame.time.Clock()
        #精灵组

        self.all_sprites = CameraGroup()

        # 植物组
        self.plant_group = pygame.sprite.Group()
        self.emotes_group = pygame.sprite.Group()
        self.talk_group = pygame.sprite.Group()
        self.bling_group = pygame.sprite.Group()
        # self.all_sprites.add(self.emotes_group)
        # 碰撞精灵组
        self.collision_sprites = pygame.sprite.Group()
        # 游戏状态 1为界面状态，2为游戏状态, 0为结束状态
        self.game_state = 1
        # player的初始化被放入setup函数中
        self.player = None
        # 土地网格，在setup中初始化
        self.soil_layer = None
        # 树的精灵组
        self.tree_sprites = pygame.sprite.Group()
        # 雨天
        self.if_rain = False
        self.rain = Rain(self.all_sprites)
        # 增加地图
        self.setup()
        # 增加BGM
        self.bgm = pygame.mixer.Sound('asset/audio/恬静的小乡村   自然声 吉他BGM - 1.Ι 风景优美 阳光明媚的下午 Ι 安静祥和的乡村氛围(Av550320855,P1).mp3')
        self.bgm.play(loops=-1)


    def setup(self):
        # 生成地图（简单背景）
        map_list = [pygame.image.load('asset/map.png').convert_alpha(), pygame.image.load('asset/blend_start.png').convert_alpha(), pygame.image.load('asset/blend_mid.png').convert_alpha(), pygame.image.load('asset/blend_end.png'), pygame.image.load('asset/map_winter.png')]
        self.map = Map(
            pos=(0, 0),
            surf=map_list,
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

        # 读取地图
        tmx_data = load_pygame('asset/map.tmx')

        # 读取地图中的树并创建树的精灵
        for obj in tmx_data.get_layer_by_name('tree'):
            Tree(pos=(obj.x, obj.y), surf=obj.image, groups=[self.all_sprites, self.collision_sprites, self.tree_sprites], name=obj.name)

        # 边缘空气墙
        for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
            Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups= self.collision_sprites)

        # 读取地图的开始点并设置人物坐标为此坐标
        for obj in tmx_data.get_layer_by_name('objects'):
            if obj.name == 'start':
                start = obj
            if obj.name == 'robot':
                trader = Generic(pos=(obj.x, obj.y), surf=pygame.transform.scale(pygame.image.load('asset/objects/robot..png').convert_alpha(), (64, 64)), groups= [self.all_sprites, self.collision_sprites])

        # 土地网格初始化New 移动位置
        self.soil_layer = SoilLayer(self.all_sprites, self.plant_group, self.collision_sprites, self.bling_group)
        # 添加人物#New新添参数
        self.player = MainCharacter(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, (start.x, start.y), self.all_sprites, self.collision_sprites, self.soil_layer, self.tree_sprites, trader)
        #New 初始道具
        self.player.gainItem(Item("Hoe"))
        self.player.gainItem(Item("Axe"))
        self.player.gainItem(Item("Pot"))
        self.player.gainItem(Item("Seed_fruittree"))

        #New 初始化聊天框
        self.trader_text_bar = TextBar(self.screen)


    def run_game(self):
        # 游戏循环，保证游戏开始运行时不会终止
        while self.game_state != 0:
            # 设置刷新帧率
            self.clock.tick(60)
            # 检查游戏事件
            self.check_event()
            # 绘制屏幕
            if self.game_state != 0:  # 这步需要再判断因为游戏可能在check_event()函数中关闭，如果关闭会导致此函数报错
                #New 实时更新player位置给camera

                runtime =pygame.time.get_ticks() // 1000
                # print(runtime)
                # print('runtime')
                runtimes = int(runtime)
                # 获取当前季节
                global current_season
                current_season = season(runtime)
                self.map.change(current_season)
                self.run_Plants(current_season, self.all_sprites)
                self.player.update_to_camera()
                self.update_screen()

                # 获取游戏运行的时间

                # 判断是否启用下雨
                if self.if_rain:
                    self.rain.update()
                    self.soil_layer.water_all()



    def update_screen(self):
        if self.game_state == 1:
            # 更新屏幕上的图像，并切换到新屏幕
            self.main_menu.draw_menu()
            # 让最近绘制的屏幕可见
        elif self.game_state == 2:
            # 渲染精灵组中所有的精灵
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update()
            # self.plant_group.draw(self.screen)
            global current_season
            self.plant_group.update(current_season)
            # self.emotes_group.update()
            # 低层环境人物绘制
            global need_moveWithMouse
            global movement
            #删除了人物display的部分 避免重复绘制
            if len(movement) != 0:
                self.player.move_by_dire(movement[len(movement) - 1])
            # 最高层UI绘制

            if self.game_state == 2:
                # New 获取物品动画
                if self.player.gainItemAnimating:
                    self.player.noticeGain(1000, self.player.new_item.num)

            if self.game_state == 2:
                #New 物品获取动画
                if self.player.gainItemAnimating:
                    self.player.noticeGain(1000, self.player.new_item.num)
                    

                if self.player.backpack.opened:
                    self.player.backpack.display()
                # New
                if self.player.shop.opened:
                    self.player.shop.display()

                self.player.inventory.display()
                if need_moveWithMouse:
                    self.player.backpack.moveWithMouse(self.player.backpack.item_chose, self.mouse_pos[0],self.mouse_pos[1])
                # New
                self.player.goldShow()

                if self.player.text_bar_show:
                    self.trader_text_bar.draw()




        pygame.display.flip()


    def check_event(self):

        global need_moveWithMouse
        global movement
        # 添加自定义事件用于测试
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.game_state = 0
                pygame.quit()

            #New 人物动画中不交互
            if self.player.text_bar_show:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.text_bar_show = False
            elif self.player.item_animating:
                continue
            #打开商店页面后的判定
            elif self.player.shop.opened:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.shop.moveChose(-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.shop.moveChose(1, 0)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.shop.moveChose(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.shop.moveChose(0, 1)
                    elif event.key == pygame.K_ESCAPE:
                        self.player.shop.closeShop()
                    elif event.key == pygame.K_SPACE:
                        if self.player.shop.state:
                            self.player.shop.sell()
                        else:
                            self.player.shop.buy()
                #商店页面切换判断
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.player.shop.buy_button.checkClick(mouse_pos[0], mouse_pos[1])
                    self.player.shop.sell_button.checkClick(mouse_pos[0], mouse_pos[1])
                    
            # 打开背包后的判定
            elif self.player.backpack.opened:
                need_moveWithMouse = False
                if self.player.backpack.item_chose != None:
                    self.mouse_pos = pygame.mouse.get_pos()
                    need_moveWithMouse = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                    start_space = self.player.backpack.checkMouseChose(self.mouse_pos)
                    if start_space != None:
                        self.player.backpack.item_chose = start_space.item

                    else:
                        self.player.backpack.item_chose = None

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pos = pygame.mouse.get_pos()
                    end_space = self.player.backpack.checkMouseChose(self.mouse_pos)
                    if end_space != None:
                        self.player.backpack.item_switch = end_space.item
                    else:
                        self.player.backpack.item_switch = None
                        self.player.backpack.display()
                    self.player.backpack.switchItem(end_space, self.player.backpack.item_chose, self.player.backpack.item_switch)
                    self.player.backpack.item_chose = None
                    self.player.backpack.item_switch = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.backpack.moveChose(-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.backpack.moveChose(1, 0)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.backpack.moveChose(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.backpack.moveChose(0, 1)
                    elif event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                        self.player.backpack.closeBackpack()
                        self.player.move(0, 0)

            # 鼠标判定
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.main_menu.play_button.available:
                    self.main_menu.play_button.check_button(self, mouse_pos)
                # 鼠标判定
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.main_menu.play_button.available:
                        self.main_menu.play_button.check_button(self, mouse_pos)
                    if event.button == 1:  # 鼠标左键点击
                        # 获取鼠标点击位置
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_pos = pygame.math.Vector2(mouse_x, mouse_y) + self.all_sprites.offset
                        # 进行碰撞检测，判断鼠标是否与某个Plant实例相交
                        clicked_sprites = [sprite for sprite in self.plant_group if
                                           sprite.rect.collidepoint(mouse_pos)]
                        # if clicked_sprites.life>800:
                        # 调用处理鼠标点击的方法
                        self.handle_mouse_click_happy(mouse_pos)
                        # else:
                        #     self.handle_mouse_click_loveu(mouse_pos)
                    elif event.button == 3:  # 鼠标右键点击
                        # 获取鼠标点击位置
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_pos = pygame.math.Vector2(mouse_x, mouse_y) + self.all_sprites.offset
                        print(f'鼠标当前位置{mouse_x},{mouse_y}')
                        # 进行碰撞检测，判断鼠标是否与某个Plant实例相交
                        clicked_sprites = [sprite for sprite in self.plant_group if
                                           sprite.rect.collidepoint(mouse_pos)]
                        # print('talk碰撞检测')
                        # print(f'{clicked_sprites}')
                        # print(f'{self.plant_group}')
                        # if clicked_sprites.life>800:
                        # 调用处理鼠标点击的方法
                        self.handle_mouse_click_talk(mouse_pos)


            # 键盘按键判定
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    movement.append(2)
                    self.player.move(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    movement.append(3)
                    self.player.move(1, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    movement.append(0)
                    self.player.move(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    movement.append(1)
                    self.player.move(0, 1)
                elif event.key == pygame.K_TAB:
                    self.player.openBackpack()
                    movement = []
                # 物品栏切换判断
                elif event.key == pygame.K_1:
                    self.player.equipItem(0)
                elif event.key == pygame.K_2:
                    self.player.equipItem(1)
                elif event.key == pygame.K_3:
                    self.player.equipItem(2)
                elif event.key == pygame.K_4:
                    self.player.equipItem(3)
                elif event.key == pygame.K_5:
                    self.player.equipItem(4)
                # New 交互按键判定
                elif event.key == pygame.K_SPACE:
                    movement = []
                    self.player.interaction()

                # 按下P键生成新的'fruittree'实例
                elif event.key == pygame.K_p:
                    self.plant_tree('fruittree')

                # 按下O键生成新的'greentree'实例
                elif event.key == pygame.K_o:
                    self.plant_tree('fruittree')

                elif event.key == pygame.K_l:
                    self.plant_crop('corn')

                #New 增加雨天天气开关
                elif event.key == pygame.K_r:

                    self.if_rain = not self.if_rain

                    # self.if_rain ^= True
                    self.plant_rain()



            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and 2 in movement:
                    movement.remove(2)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and 3 in movement:
                    movement.remove(3)
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and 0 in movement:
                    movement.remove(0)
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and 1 in movement:
                    movement.remove(1)
                # 在鼠标左键点击处生成新的'fruittree'实例

    def handle_mouse_click_happy(self, mouse_pos):
        # 获取相交的Plant实例
        clicked_sprites = [sprite for sprite in self.plant_group if sprite.rect.collidepoint(mouse_pos)]

        if clicked_sprites:
            clicked_sprite = clicked_sprites[0]  # 获取第一个相交的Plant实例
            # 检查是否已经存在Emotes实例，如果存在，则重新设置属性，否则创建新的Emotes实例
            # if clicked_sprite.emotes is not None:
            #     for emote in clicked_sprite.emotes:
            #         clicked_sprite.emotes.emote.haverun_num = 0  # 重新设置表情动画的属性
            # else:
                # 创建Emotes实例
            if clicked_sprite.life>800:
                new_emotes = Emotes(mouse_pos,'happy', [self.emotes_group, self.all_sprites])
            else:
                new_emotes = Emotes(mouse_pos, 'loveu', [self.emotes_group, self.all_sprites])
                # 将Emotes实例添加到emotes_group中
            self.emotes_group.add(new_emotes)
                # 将Emotes实例赋值给clicked_sprite.emotes
            clicked_sprite.emotes.append(new_emotes)

    def handle_mouse_click_talk(self, mouse_pos):
        # 获取相交的Plant实例
        clicked_sprites = [sprite for sprite in self.plant_group if sprite.rect.collidepoint(mouse_pos)]

        if clicked_sprites:
            clicked_sprite = clicked_sprites[0]  # 获取第一个相交的Plant实例
            print('已经有clicked_sprites')
            new_talk = Talk(mouse_pos, [self.talk_group, self.all_sprites])
            # 将Emotes实例添加到emotes_group中
            print('已经创建新emotes实例')
            self.talk_group.add(new_talk)
            # 将Emotes实例赋值给clicked_sprite.emotes
            clicked_sprite.talk.append(new_talk)
    def run_Plants(self,current_season, all_sprites):
        for plant in self.plant_group:
            plant.plant_update(current_season, self.all_sprites)
            # for new_emotes in self.emotes_group:

            plant.emotes_update()
            # if plant.life > 100:#高血量（表情）
            #     print('血量大于800')
            #     # 在植物位置生成情感动画
            plant.emotes_update()
            plant.bling_update()
            plant.talk_update()
            if plant.tree == 0:
                plant.plant_harvest_update(current_season, self.all_sprites)

            if plant.death():
                # 将土地重新恢复成可种植的样子
                x, y = plant.pos
                x = x // TILE_SIZE
                y = y // TILE_SIZE
                self.soil_layer.grid[y][x].remove('P')
                self.soil_layer.grid[y][x].remove(plant)

    def plant_tree(self,plant_type):#生成树
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_plant = Plant(f'{plant_type}', [self.plant_group, self.all_sprites, self.collision_sprites],
                          pygame.math.Vector2(mouse_x, mouse_y) + self.all_sprites.offset)
        self.plant_group.add(new_plant)
        # new_emotes = Emotes(groups=[emotes_group, self.all_sprites], pos=new_plant.rect.topright)
        # emotes_group.add(new_emotes)
        # new_plant.emotes = new_emotes
    def plant_crop(self,plant_type): #生成作物
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_crop = Crop(f'{plant_type}', [self.plant_group, self.all_sprites, self.collision_sprites],
                          pygame.math.Vector2(mouse_x, mouse_y) + self.all_sprites.offset)
        self.plant_group.add(new_crop)
        print('已生成植物')
        print(f'作物rect:{new_crop.rect}')

    def plant_rain(self):
        starttime = 0
        now_time = pygame.time.get_ticks()
        delay = 5000
        if now_time-starttime>=delay:
            self.if_rain ^= True
            starttime=pygame.time.get_ticks()

def season(runtimes):
    # 规定每个季节的持续时间为10秒
    per_season = 5

    # 计算当前季节的编号，从1开始，分别代表春天、夏天、秋天和冬天
    cal_season = (runtimes // per_season) % 4 + 1

    return cal_season #cal指的是计算出的
if __name__ == '__main__':
    game = ForestGarden()
    game.run_game()
