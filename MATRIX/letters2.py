import time
import pygame as pg
import random as rnd
import sys
import time as t
from window_size import size_window
pg.init()
#-----------------
#создаем и тут катканский алфавит с другими символами
katakana = [chr(j) for j in range(int('0x30a0', 16), (int('0x30a0', 16) + 96))]
numbers = [str(i) for i in range(10)]
flags = ['-', '+', '=', '!', '&', '?', '<', '>', '@']
general_list = katakana + numbers + flags
#----------------
#класс одного символа
class LETTER(pg.sprite.Sprite):
    def __init__(self, x, y, let, color, group, speed, WS):
        self.color = color #цвет
        self.let = let #символ
        self.group = group #группа
        self.x, self.y = x, y #координаты
        self.WS = WS #шрифт
        pg.sprite.Sprite.__init__(self)
        self.image = pg.font.SysFont('pingfang', self.WS).render(self.let, True, self.color)
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self.add(self.group)
        self.speed = speed
    def update(self, *first_letter):
        self.rect.y += self.speed
        self.interval = rnd.randint(10, 50)
        #если переменная равна 20 то image меняется и перезапиывается (обязательно в условии, иначе будет сильно лагать
        if self.interval == 20:
            self.let = rnd.choice(general_list)
            self.image = pg.font.SysFont('pingfang', self.WS).render(self.let, True, self.color)
        #объект удаляется из группы если выходит за нижнюю границу окна
        self.kill() if self.rect.y > size_window()[1] else self.rect.y

