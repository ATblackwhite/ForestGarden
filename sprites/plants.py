import os
import pygame
import sys
import re
from settings import PLANT_ATTRIBUTE,LAYERS
from sprites.generic import Generic

# def import_folder(folder_path):
#     animation_images = []
#     for filename in sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r'\d+', x)[0])):
#         image_path = os.path.join(folder_path, filename)
#         image = pygame.image.load(image_path)
#         scaled_image = pygame.transform.scale(image, (192,320))
#         animation_images.append(scaled_image)
#         image_rect = scaled_image.get_rect()
#         image_rect.midbottom = (192 // 2, 320)
#
#         animation_images.append((scaled_image, image_rect))
#     return animation_images
def import_folder(folder_path):
    animation_images = []
    for filename in sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r'\d+', x)[0])):
        image_path = os.path.join(folder_path, filename)
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (192, 320))
        animation_images.append(scaled_image)
    return animation_images

# 定义Plant类继承自pygame.sprite.Sprite
class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, pos):
        super().__init__(groups)

        # setup
        self.plant_type = plant_type
        self.frames = import_folder(f'sources\Plants/{plant_type}')
        self.pos = pos

        # plant growing
        self.stage = 0
        self.grow_speed, self.life, self.stages = PLANT_ATTRIBUTE.get(plant_type)
        self.growth = float(0)

        # sprite setup
        self.image = self.frames[self.stage]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=pos + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['fruit']


        # hitbox setup
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.8)
        self.hitbox.bottom = self.rect.bottom

    def update(self,current_season):
        # 更新植物的生长状态和图像
        self.growth += self.grow_speed
        if self.growth < 1:
            self.stage = 0
            print('stage0')
            print(current_season)
        elif self.growth < 2:
            self.stage = 1
            print('s1')
            print(current_season)
        elif self.growth < 3:
            self.stage = 2
            print('s2')
            print(current_season)
        elif self.growth < 4:
            self.stage = 3
            print('s3')
            print(current_season)
        elif self.growth>=4:
            if current_season == 1:
                self.stage = 4
                print('s4')
            elif current_season == 2:
                self.stage = 5
                print('s5')
            elif current_season == 3:
                self.stage = 6
                print('s6')
            elif current_season == 4:
                self.stage = 7
                print('s7')

        self.image = self.frames[int(self.stage)]
        # 更新hitbox位置
        self.hitbox.midbottom = self.pos + pygame.math.Vector2(0, self.y_offset)


    def death(self):
        # 执行植物死亡的相关操作
        self.life -= 1
        if self.life <= 0:
            print(f"位置在{self.pos}的植物死了。")
            self.kill()  # 删除该植物实体
# class emotes(Plant):
#     def __init__(self,z,plant,duration=200):
#         super().__init__(z,plant.rect.topright)
#         self.start_time = pygame.time.get_ticks()
#         self.duration = duration
#         self.emotion_frames = import_folder(f'sources\Plants/emotes')  # Replace 'emotion' with the folder name for emotion animations
#         self.emotion_frame_index = 0
#         self.emotion_frame_delay = 100  # Adjust this value to control the speed of emotion animation
#         self.emotion_last_update = pygame.time.get_ticks()
#         self.emotion_image_size = (64, 64)  # Replace with the desired size for the emotion animation images
#         self.image = self.emotion_frames[self.emotion_frame_index]
#     def update(self):
#         current_time = pygame.time.get_ticks()
#         # if Plant.__init__().life:
#         #     self.kill()
#
#         if current_time - self.emotion_last_update >= self.emotion_frame_delay:
#             self.emotion_frame_index = (self.emotion_frame_index + 1) % len(self.emotion_frames)
#             self.image = pygame.transform.scale(self.emotion_frames[self.emotion_frame_index], self.emotion_image_size)
#             self.emotion_last_update = pygame.time.get_ticks()
#             print('emo')
class Emotes(pygame.sprite.Sprite):
    def __init__(self,pos,duration=200, groups=None):
        super().__init__(groups)  # Call the constructor of the Plant class with 'emotes' as the plant_type
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.emotion_frames = import_folder(f'sources/Plants/emotes')
        self.emotion_frame_index = 0
        self.emotion_frame_delay = 100
        self.emotion_last_update = 0
        self.emotion_image_size = (64, 64)
        self.pos = pos
        self.z = LAYERS['rain drops']
        self.y_offset = -16
        self.image = self.emotion_frames[self.emotion_frame_index]  # 修改部分：在这里设置self.image
        self.rect = self.image.get_rect(midbottom=pos + pygame.math.Vector2(0, self.y_offset) )

    def update(self):
        current_time = pygame.time.get_ticks()
        # if current_time - self.start_time >= self.duration
        # :
        #     self.kill()

        if current_time - self.emotion_last_update >= self.emotion_frame_delay:
            self.emotion_frame_index = (self.emotion_frame_index + 1) % len(self.emotion_frames)
            self.image = pygame.transform.scale(self.emotion_frames[self.emotion_frame_index], self.emotion_image_size)
            self.rect = self.image.get_rect(midbottom=self.pos + pygame.math.Vector2(0, self.y_offset))
            self.emotion_last_update = current_time
            print('runle')


