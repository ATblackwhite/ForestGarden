import pygame.sprite

from UI.interface.mainMenu import MainMenu
from character.MainCharacter import *

from settings import *
from camera.cameraGroup import CameraGroup
from sprites.generic import Generic
from sprites.tree import Tree
from pytmx.util_pygame import load_pygame
from camera.soilLayer import SoilLayer

movement = []
need_moveWithMouse = False

class FroestGarden:
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
        # 碰撞精灵组
        self.collision_sprites = pygame.sprite.Group()
        # 游戏状态 1为界面状态，2为游戏状态
        self.game_state = 1
        # NEW player的初始化被放入setup函数中
        self.player = None
        # NEW 土地网格，在setup中初始化
        self.soil_layer = None
        # 增加地图
        self.setup()


    def setup(self):
        # 生成地图（简单背景）
        Generic(
            pos=(0, 0),
            # surf=pygame.image.load('sources/UI/world/ground.png').convert_alpha(),
            surf=pygame.image.load(r"asset/map.png").convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

        # 读取地图
        tmx_data = load_pygame('asset/map.tmx')

        # 读取地图中的树并创建树的精灵
        for obj in tmx_data.get_layer_by_name('tree'):
            Tree(pos=(obj.x, obj.y), surf=obj.image, groups=[self.all_sprites, self.collision_sprites], name=obj.name)

        # 边缘空气墙
        for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
            Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=self.collision_sprites)
        #
        # 读取地图的开始点并设置人物坐标为此坐标
        for obj in tmx_data.get_layer_by_name('objects'):
            if obj.name == 'start':
                start = obj
        # 添加人物
        self.player = MainCharacter(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, (start.x, start.y), self.all_sprites)

        # 土地网格初始化
        self.soil_layer = SoilLayer(self.all_sprites)


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
                self.player.update_to_camera()
                self.update_screen()

    def update_screen(self):
        if self.game_state == 1:
            # 更新屏幕上的图像，并切换到新屏幕
            self.main_menu.draw_menu()
            # 让最近绘制的屏幕可见
        elif self.game_state == 2:
            # 渲染精灵组中所有的精灵
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update()
            # 低层环境人物绘制
            global need_moveWithMouse
            global movement
            #New 删除了人物display的部分 避免重复绘制
            if len(movement) != 0:
                self.player.move_by_dire(movement[len(movement) - 1])
            # 最高层UI绘制
            if self.game_state == 2:
                if self.player.backpack.opened:
                    self.player.openBackpack()
                self.player.inventory.display()
                if need_moveWithMouse:
                    self.player.backpack.moveWithMouse(self.player.backpack.item_chose, self.mouse_pos[0],
                                                       self.mouse_pos[1])

        pygame.display.flip()

    def check_event(self):

        global need_moveWithMouse
        global movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = 0
                pygame.quit()

            # 打开背包后的判定
            if self.player.backpack.opened:
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
                    elif event.key == pygame.K_TAB:
                        self.player.backpack.opened = False
                        self.player.move(0, 0)

            # 鼠标判定
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.main_menu.play_button.available:
                    self.main_menu.play_button.check_button(self, mouse_pos)

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
                #物品栏切换判断
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

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    movement.remove(2)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    movement.remove(3)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    movement.remove(0)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    movement.remove(1)


if __name__ == '__main__':
    game = FroestGarden()
    game.run_game()
