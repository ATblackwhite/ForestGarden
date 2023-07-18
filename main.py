import pygame
from Button import Button
from MainCharacter import MainCharacter

movement = []
class FroestGarden:
    # 管理游戏的类
    def __init__(self):
        # 初始化游戏
        pygame.init()
        self.screen = pygame.display.set_mode((683, 384))
        # 设置游戏标题
        pygame.display.set_caption("Forest Garden")
        # 设置游戏的背景
        self.back_ground = pygame.transform.scale(pygame.image.load(r"sources\UI\background\background.png"), (683, 384))
        # 按钮设置
        self.play_button = Button(self, "play")
        # 添加系统时钟
        self.clock = pygame.time.Clock()
        # 游戏状态 1为界面状态，2为游戏状态
        self.game_state = 1
        # 添加人物
        self.player = MainCharacter(683, 384, self.screen)

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
            #让最近绘制的屏幕可见
        elif self.game_state == 2:
            if len(movement) != 0:
                self.player.move_by_dire(movement[len(movement) - 1])
        pygame.display.flip()

    def check_event(self):
        if len(movement) != 0:
            self.player.move_by_dire(movement[len(movement) - 1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = 0
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.available:
                    self.play_button.check_button(self, mouse_pos)
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
