import os
import pygame
import sys
import re

from settings import PLANT_ATTRIBUTE, LAYERS

from settings import PLANT_ATTRIBUTE,LAYERS
from sprites.particle import Particle

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
        self.y_offset = -16 #if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=pos + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['fruit']


        # hitbox setup
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.8)
        self.hitbox.bottom = self.rect.bottom


    def update_plant(self, current_season):

        #表情：
        self.emotes = []
        self.last_emotes_time = 0  # 记录上一次执行emotes_update()的时间
        self.emotes_delay = 600  # 设置延迟时间（毫秒）
        self.video_frame = 0
        # self.last_time = 0
        # self.delay = 150
        # self.frame_num = 0
        # self.haverun_num = 0

        self.stump_origin_image = pygame.image.load(f'sources/Plants/stump/1.png')
        self.stump_image = pygame.transform.scale(self.stump_origin_image, (120, 240))

    def plant_update(self,current_season):

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
            if self.emotes is not None:
                for emote in self.emotes:
                    emote.kill()
            self.image = self.stump_image
            # 删除该植物实体
            # for emote in self.emotes:
    def damage(self):
        if self.life>0:
            self.life -= 500
            Particle(
                pos=self.rect.topleft,
                surf=self.image,
                groups=self.all_sprites,  # self.groups()[1]是all_sprites组
                z=LAYERS['fruit']
            )
            if self.health <= 0:
                self.image = self.stump_image
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.9, -self.rect.height * 0.6)


    def add_emotes(self, pos, groups):
        # 将Emotes实例添加到self.emotes列表中
        emotes_instance = Emotes(pos, groups)
        self.emotes.append(emotes_instance)

    def emotes_update(self, frame_num=4):
        frame_num = frame_num

        # 遍历self.emotes列表中的每个Emotes实例
        for emotes_instance in self.emotes:
            if emotes_instance.haverun_num <= frame_num:
                current_time = pygame.time.get_ticks()
                if current_time - emotes_instance.last_time > emotes_instance.emotion_frame_delay:
                    emotes_instance.emotion_frame_index = (emotes_instance.emotion_frame_index + 1) % len(emotes_instance.emotion_frames)
                    emotes_instance.image = pygame.transform.scale(emotes_instance.emotion_frames[emotes_instance.emotion_frame_index],emotes_instance.emotion_image_size)
                    print('图片已经切换')
                    emotes_instance.last_time = pygame.time.get_ticks()
                    emotes_instance.haverun_num += 1
            else:
                # 表情动画播放完成后，删除表情实例
                emotes_instance.kill()

class Emotes(pygame.sprite.Sprite):
    def __init__(self,pos,emo_type,groups):
        super().__init__(groups)  # Call the constructor of the Plant class with 'emotes' as the plant_type
        self.start_time = pygame.time.get_ticks()
        self.emotion_frames = import_folder(f'sources/Plants/emotion/{emo_type}')
        self.emotion_frame_index = 0
        self.emotion_frame_delay = 100
        self.last_time = 0
        self.haverun_num = 0
        self.emotion_image_size = (64, 64)
        self.pos = pos
        self.z = LAYERS['rain drops']
        self.y_offset = -16
        self.image = self.emotion_frames[self.emotion_frame_index]  # 修改部分：在这里设置self.image
        self.rect = self.image.get_rect(midbottom=pos)







