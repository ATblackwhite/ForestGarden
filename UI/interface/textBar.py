import pygame

from settings import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class TextBar:
    def __init__(self, screen):
        self.screen = screen

        # 定义对话框的尺寸和位置
        self.dialogue_box_width, self.dialogue_box_height = 800, 150
        self.dialogue_box_x, self.dialogue_box_y = (SCREEN_WIDTH - self.dialogue_box_width) // 2, SCREEN_HEIGHT - self.dialogue_box_height - 50

        # 定义对话文本
        self.dialogue_text = "Hello, I am BT-7274. You     can buy or sell items from me."

        # 加载字体
        self.font = pygame.font.Font(r'C:\Users\16218\Documents\GitHub\ForestGarden\sources\UI\UIPack\Font\kenvector_future.ttf', 30)

        # 分割对话文本为逐句显示
        self.dialogue_lines = [char for char in self.dialogue_text]
        self.current_line = ''
        self.lines_to_display = []

        # 加载自定义的对话框图片
        self.dialogue_box_image = pygame.transform.scale(pygame.image.load(r"asset\objects\letterBG..png").convert_alpha(), (self.dialogue_box_width, self.dialogue_box_height))

        # 创建时间
        self.last_time = pygame.time.get_ticks()

    def draw(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 50:
            self.last_time = current_time
            if self.dialogue_lines:
                self.current_line += self.dialogue_lines.pop(0) + ' '
                if self.current_line[0] == ' ':
                    self.current_line = self.current_line[1:]
                text_surface = self.font.render(self.current_line, True, WHITE)
                # 换行
                if text_surface.get_width() > self.dialogue_box_width - 50:
                    self.lines_to_display.append(self.current_line)
                    self.current_line = ''
        # 绘制自定义对话框图片
        self.screen.blit(self.dialogue_box_image, (self.dialogue_box_x, self.dialogue_box_y))
        for i, line in enumerate(self.lines_to_display):
            text_surface = self.font.render(line, True, BLACK)
            self.screen.blit(text_surface, (self.dialogue_box_x + 30, self.dialogue_box_y + 30 + i * 30))
        current_text_surface = self.font.render(self.current_line, True, BLACK)
        self.screen.blit(current_text_surface, (self.dialogue_box_x + 30, self.dialogue_box_y + 30 + len(self.lines_to_display) * 30))