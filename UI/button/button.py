import pygame
class Button:
    def __init__(self, game, msg, width, height):
        # 初始化按钮属性
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.width = width
        self.height = height
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # 按钮标签只需创建一次
        self.prep_msg(msg)
        # 判断按钮是否继续工作
        self.available = True

    def prep_msg(self, msg):
        # 将msg渲染成图像，并使其在按钮上居中
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

