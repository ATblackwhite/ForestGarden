import pygame

def displayText(txt, screen, height, start_x, start_y, size=24, Font='sources/UI/UIPack/Font/kenvector_future.ttf'):
    text = txt[:]
    if Font == "":
        font = pygame.font.Font(size=size)
    else:
        font = pygame.font.Font(Font, size=size)
    line_number = 0
    for i in text.split('\n'):
        line = font.render(i, True, (0, 0, 0))
        screen.blit(line, (start_x, start_y+height*line_number))
        line_number += 1
