import os
import random

import pygame
import sys
import re
from settings import PLANT_ATTRIBUTE, LAYERS
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
        self.frames = import_folder(f'sources\plants/{plant_type}')
        self.pos = pos

        # plant growing
        self.stage = 0
        self.grow_speed, self.life, self.stages = PLANT_ATTRIBUTE.get(plant_type)[:3]
        self.growth = float(0)

        # sprite setup
        self.image = pygame.transform.scale(self.frames[self.stage],(192,320))
        self.y_offset = -16 + 70  # +50是因为需要修正显示位置，下面的30同理  #if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=pos + pygame.math.Vector2(30, self.y_offset))
        self.z = LAYERS['fruit']


        # hitbox setup
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.height * 0.8)
        self.hitbox.bottom = self.rect.bottom
        self.hitbox.x += 30


        #表情：
        self.emotes = []
        self.last_emotes_time = 0  # 记录上一次执行emotes_update()的时间
        self.emotes_delay = 600  # 设置延迟时间（毫秒）
        self.video_frame = 0
        # self.last_time = 0
        # self.delay = 150
        # self.frame_num = 0
        # self.haverun_num = 0

        #树桩
        self.stump_origin_image = pygame.image.load(f'sources/plants/stump/1.png')
        self.stump_image = pygame.transform.scale(self.stump_origin_image, (120, 240))

        #生长动画
        self.last_stage = 0
        self.stagevideo = []

        #好感度
        self.love_player = 0

        #是否为树
        self.tree =1
        self.harvestable = 0

        #talk
        self.talk = []
        self.talk_num = 1

        self.relationship = 1
        self.relationword = None
        self.stageword = None
        self.seasonword = None
        self.talkword = (f'{self.stageword}')
        self.water = 1

        #
        self.sound = pygame.mixer.Sound('sources/Plants/music/plant.mp3')
        self.last_stage = 0

    def plant_update(self, current_season, bling_groups):
        # 更新植物的生长状态和图像
        self.growth += self.grow_speed
        if self.growth < 1:
            self.stage = 0

        elif self.growth < 2:
            self.stage = 1

        elif self.growth < 3:
            self.stage = 2

        elif self.growth < 4:
            self.stage = 3

        elif self.growth >= 4:
            if current_season == 1:
                self.stage = 4

            elif current_season == 2:
                self.stage = 5

            elif current_season == 3:
                self.stage = 6

            elif current_season == 4:
                self.stage = 7

        if self.last_stage < self.stage:
            bling = Bling(self.rect.midbottom + pygame.Vector2(50, 200), bling_groups, 'green')
            self.stagevideo.append(bling)
            self.last_stage = self.stage

        # 植物本身图片
        self.image = self.frames[int(self.stage)]
        # 更新hitbox位置
        self.hitbox.midbottom = self.pos + pygame.math.Vector2(0, self.y_offset)
        self.hitbox.x += 30

    def death(self):
        # 执行植物死亡的相关操作
        self.life -= 1
        if self.life <= 0:
            print(f"位置在{self.pos}的植物死了。")
            if self.emotes is not None:
                for emote in self.emotes:
                    emote.kill()
            self.kill()
            return True
        return False

        # 删除该植物实体
        # for emote in self.emotes:
    def talk_relation(self):#标记
        if self.relationship<20:
            self.relationword = 'normal'
        elif self.relationship>=20:
            self.relationword = 'good'
        elif self.relationship>=80:
            self.relationword = 'deep'##
        return self.relationword

    def talk_stage(self):
        if self.life>=18000:
            self.stageword = 'baby'
        elif 5000<self.life<18000:
            if self.harvestable == 0:
                self.stageword = 'young'
            elif self.harvestable ==1:
                self.stageword = 'harvest'
            else:
                self.stageword = 'young'
        elif self.life<5000:
            self.relationword = 'old'###
        return self.stageword
    def talk_season(self,current_season):
        if current_season ==1:
            self.seasonword = 'spring'
        elif current_season ==2:
            self.seasonword = 'summer'
        elif current_season ==3:
            self.seasonword = 'authmn'
        elif current_season ==4:
            self.seasonword = 'winter'
        return self.seasonword
    def damage(self):
        if self.life > 0:
            self.life -= 500
            Particle(
                pos=self.rect.topleft,
                surf=self.image,
                groups=self.all_sprites,  # self.groups()[1]是all_sprites组
                z=LAYERS['fruit']
            )
            if 0 < self.life <= 200:
                self.image = self.stump_image
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.9, -self.rect.height * 0.6)

    def plant_play_sound(self):
        if self.last_stage !=self.stage:
            self.sound.play()
            self.last_stage = self.stage


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
                    emotes_instance.emotion_frame_index = (emotes_instance.emotion_frame_index + 1) % len(
                        emotes_instance.emotion_frames)
                    emotes_instance.image = pygame.transform.scale(
                        emotes_instance.emotion_frames[emotes_instance.emotion_frame_index],
                        emotes_instance.emotion_image_size)
                    print('图片已经切换')
                    emotes_instance.last_time = pygame.time.get_ticks()
                    emotes_instance.haverun_num += 1
            else:
                # 表情动画播放完成后，删除表情实例
                emotes_instance.kill()

    def bling_update(self):
        # 遍历self.emotes列表中的每个Emotes实例
        for bling_instance in self.stagevideo:
            if bling_instance.frames_num_now <= bling_instance.frames_num:
                current_time = pygame.time.get_ticks()
                if current_time - bling_instance.last_time > bling_instance.frame_delay:
                    bling_instance.frame_index = (bling_instance.frame_index + 1) % len(bling_instance.bling_frames)
                    bling_instance.image = pygame.transform.scale(
                        bling_instance.bling_frames[bling_instance.frame_index], bling_instance.image_size)
                    print('图片已经切换')
                    bling_instance.last_time = pygame.time.get_ticks()
                    bling_instance.frames_num_now += 1
            else:
                # 表情动画播放完成后，删除表情实例
                bling_instance.kill()
    def talk_update(self):
        # 遍历self.talk列表中的每个Talk实例
        for talk_instance in self.talk:
            if talk_instance.frames_num_now <= talk_instance.frames_num:
                current_time = pygame.time.get_ticks()
                if current_time - talk_instance.last_time > talk_instance.frame_delay:
                    # talk_instance.frame_index = (talk_instance.frame_index + 1) % len(talk_instance.talk_frames)
                    talk_instance.frame_index = random.randrange(0,len(talk_instance.talk_frames))
                    talk_instance.image = pygame.transform.scale(talk_instance.talk_frames[talk_instance.frame_index],
                                                                 talk_instance.long_sentence_size)
                    print('图片已经切换')
                    talk_instance.last_time = pygame.time.get_ticks()
                    talk_instance.frames_num_now += 1
            else:
                # 表情动画播放完成后，删除表情实例
                talk_instance.kill()

class Crop(Plant):
    def __init__(self, plant_type, groups, pos):
        # 调用父类的构造函数来初始化基本属性
        super().__init__(plant_type, groups, pos)
        self.havestseason = PLANT_ATTRIBUTE.get(plant_type)[3]
        # 新增属性 self.harvestable，默认初始值为0
        self.harvestable = 0
        self.fruit = 1
        self.image = pygame.transform.scale(self.frames[self.stage],(130,217))
        self.tree = 0
        self.harvest_lasttime=0
        self.rect.center += pygame.math.Vector2(0, 50)
        self.y_offset = -16 + 50

    def plant_update(self,current_season,bling_group):
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
                self.stage = 5#有花无果
                print('s4')
            elif current_season == 2:
                self.stage = 5
                print('s5')
            elif current_season == 3 and self.fruit>=1:
                self.stage = 4
                print('成熟可收获')
            elif current_season == 3 and( self.harvestable!=1 or self.fruit<1):
                self.stage = 5
                print('s6')
            elif current_season == 4:
                self.stage = 3#无果无花
                print('s7')
        if self.last_stage < self.stage:
            bling = Bling(self.rect.midbottom+pygame.Vector2(50,200),bling_group,'green')
            self.stagevideo.append(bling)
            self.last_stage = self.stage

           #植物本身图片
        self.image = self.frames[int(self.stage)]
        # 更新hitbox位置
        self.hitbox.midbottom = self.pos + pygame.math.Vector2(0, self.y_offset)

    def plant_harvest_update(self, current_season, bling_group):
        # 新增代码：根据生长状态和季节来判断是否可以收获
        if self.growth >= 4 and self.life > 100 and self.fruit >= 1 and current_season == 3:
            self.harvestable = 1
            bling = Bling(self.rect.midbottom + pygame.Vector2(50, 200), bling_group, 'yellow')
            self.stagevideo.append(bling)
        else:
            self.harvestable = 0

    def havest_ornot(self):
        return (self.harvestable, self.plant_type)


def update_harvestable(crop, bling_groups):
    harvestable, plant_type = crop.havest_ornot()
    if harvestable == 1:
        bling = Bling(crop.rect.midbottom + pygame.Vector2(50, 200), bling_groups, 'blue')
        crop.stagevideo.append(bling)
        crop.fruit = 0
        crop.harvestable = 0
        # 设置水果度为0
        return plant_type
    elif harvestable == 0:
        crop.fruit +=0.001
        return None


class Emotes(pygame.sprite.Sprite):
    def __init__(self, pos, emo_type, groups):
        super().__init__(groups)  # Call the constructor of the Plant class with 'emotes' as the plant_type
        self.start_time = pygame.time.get_ticks()
        self.emotion_frames = import_folder(f'sources/plants/emotion/{emo_type}')
        self.emotion_frame_index = 0
        self.emotion_frame_delay = 100
        self.last_time = 0
        self.haverun_num = 0
        self.emotion_image_size = (120, 120)
        self.pos = pos
        self.z = LAYERS['rain drops']
        self.y_offset = -16
        self.image = self.emotion_frames[self.emotion_frame_index]  # 修改部分：在这里设置self.image
        self.rect = self.image.get_rect(midbottom=pos)


class Bling(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color):
        super().__init__(groups)
        self.bling_folder = f'sources/plants/bling/{color}'  # 设置 bling 文件夹路径
        self.bling_frames = import_folder(self.bling_folder)
        self.frames_num = 6
        self.frame_index = 0
        self.frame_delay = 100
        self.last_time = 0
        self.frames_num_now = 0
        self.image_size = (120, 120)
        self.image = self.bling_frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.z = LAYERS['rain drops']

class Talk(pygame.sprite.Sprite):
    def __init__(self, pos, groups,plant,current_season):
        super().__init__(groups)
        talk_stage_input = plant.talk_stage()
        talk_season_input = plant.talk_season(current_season)
        talk_relation_input = plant.talk_relation()
        self.talk_folder = f'sources/plants/talk/{talk_stage_input}/{talk_relation_input}/{talk_season_input}'  # 设置 bling 文件夹路径
        self.talk_frames = import_folder(self.talk_folder)
        self.frames_num = 1
        self.frame_index = 0
        self.frame_delay = 1500
        self.last_time = 0
        self.frames_num_now = 0
        self.long_sentence_size = (150, 150)
        self.short_sentence_size = (100, 100)
        self.image = self.talk_frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.z = LAYERS['rain drops']




