from UI.button.button import Button

class PlayButton(Button):
    def __init__(self, game):
        super().__init__(game, 'play', 200, 50)
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.width = 200
        self.height = 50


    def check_button(self, game, mouse_pos):
        # 玩家单机play按钮开始新游戏
        button_clicked = self.rect.collidepoint(mouse_pos)
        if button_clicked:
            game.game_state = 2
            print("游戏开始")
            self.available = False
            self.screen.fill((255, 255, 255))
            game.player.screen.blit(game.player.animate[1][1], (game.player.posx, game.player.posy))
