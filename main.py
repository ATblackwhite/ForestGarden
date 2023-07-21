import pygame
from UI.button.PlayButton import PlayButton
from character.MainCharacter import *
from character.Item import Item
from settings import Settings

movement = []
need_moveWithMouse = False

class FroestGarden:
    # 管理游戏的类
    def __init__(self):
        # 初始化游戏
        pygame.init()
        # 读取游戏设置
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 设置游戏标题
        pygame.display.set_caption("Forest Garden")
        # 设置游戏的背景
        self.back_ground = pygame.transform.scale(pygame.image.load(r"sources\UI\background\background.png"),
                                                  (self.settings.screen_width, self.settings.screen_height))
        # 按钮设置
        self.play_button = PlayButton(self)
        # 添加系统时钟
        self.clock = pygame.time.Clock()
        # 游戏状态 1为界面状态，2为游戏状态
        self.game_state = 1
        # 添加人物
        self.player = MainCharacter(self.settings.screen_width, self.settings.screen_height, self.screen)
        # 添加测试物品
        self.player.gainItem(Item(1))
        self.player.gainItem(Item(2))


    def run_game(self):
        # 游戏循环，保证游戏开始运行时不会终止
        while self.game_state != 0:
            # 设置刷新帧率
            self.clock.tick(60)
            # 检查游戏事件
            self.check_event()
            # 绘制屏幕
            if self.game_state != 0:  # 这步需要再判断因为游戏可能在check_event()函数中关闭，如果关闭会导致此函数报错
                self.update_screen()

    def update_screen(self):
        if self.game_state == 1:
            # 更新屏幕上的图像，并切换到新屏幕
            self.screen.blit(self.back_ground, (0, 0))
            self.play_button.draw_button()
            # 让最近绘制的屏幕可见
        elif self.game_state == 2:
            #Delete
            #if len(movement) != 0:
            #    self.player.move_by_dire(movement[len(movement) - 1])
            pygame.display.flip()
        pygame.display.flip()

    def check_event(self):

        # 低层环境人物绘制
        global need_moveWithMouse
        global movement
        self.player.screen.fill((255, 255, 255))
        if len(movement) != 0:
            self.player.move_by_dire(movement[len(movement) - 1])
            self.player.display(1)
        else:
            self.player.display(0)

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
                if self.play_button.available:
                    self.play_button.check_button(self, mouse_pos)

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
                #New 物品栏切换判断
                elif event.key == pygame.K_1:
                    self.player.equipItem(0)
                    print(self.player.equiped_item)
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
        #最高层UI绘制
        if self.player.backpack.opened:
            self.player.openBackpack()
        self.player.inventory.display()
        if need_moveWithMouse:
            self.player.backpack.moveWithMouse(self.player.backpack.item_chose, self.mouse_pos[0], self.mouse_pos[1])

if __name__ == '__main__':
    game = FroestGarden()
    game.run_game()
