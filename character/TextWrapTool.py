import pygame

def displayText(txt, screen, height, start_x, start_y):
    text = txt[:]
    font = pygame.font.Font('sources/UI/UIPack/Font/kenvector_future.ttf', 24)
    line_number = 0
    for i in text.split('\n'):
        line = font.render(i, True, (0, 0, 0))
        screen.blit(line, (start_x, start_y+height*line_number))
        line_number += 1
