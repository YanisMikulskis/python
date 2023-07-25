import pygame as pg
import random as rnd
from window_size_snake import size_window
class APPLE(pg.sprite.Sprite):
    def __init__(self,x, y, filename, size, group, color_yellow=True):
        pg.sprite.Sprite.__init__(self)
        image_start = pg.image.load(filename).convert_alpha()
        # ------------------------------------------
        self.image = pg.transform.scale(image_start, [size[0], size[1]])
        self.rect = self.image.get_rect(center = [x,y])
        self.color_int = [rnd.randint(0, 255) for _ in range(3)]
        self.color_yellow = color_yellow
        self.nx, self.ny = 1, 1
        self.boom_x = rnd.randint(-20, 20)
        self.boom_y = rnd.randint(-20, 20)
        self.applebody = None
        # ------------------------------------------
        if isinstance(group, pg.sprite.Group):
            self.add(group)
            self.applebody = False
        elif group is None:
            self.applebody = True
        #если объект тип параметра group принадлежит к классу pg.sprite.Group -
        # значит это спора и мы добавляем ее в группу. иначе - это тело яблока и в группу оно не идет
        #а переменная self apple body становится равна True для условия в функции внизу
    def update(self, boom = False, arg_kill=False):
        def outside_window():
            if self.applebody:
                if self.rect.centerx < 0 or self.rect.centerx > size_window()[0]:
                    return 1
                if self.rect.centery < 0 or self.rect.centery > size_window()[1]:
                    return 1
            else:
                return 0
        #функция - если тело яблока заходит за границы нашего окна, то оно пересоздается в центре окна
        self.rect.centerx += rnd.randint(-self.nx, self.nx)
        self.rect.centery += rnd.randint(-self.ny, self.ny)
        if outside_window():
            self.rect.center = [size_window()[0]//2, size_window()[1]//2]
        self.color_int = list(map(lambda color: color - 1 if color > 0 else color, self.color_int))
        #выше уменьшение каждого элемента списка цвета и перезапись в атрибут класса
        if boom:
            if self.boom_x > 0: self.boom_x -= 1
            elif self.boom_x < 0: self.boom_x += 1
            if self.boom_x == 0: self.boom_y += 1
            self.rect.centery += self.boom_y
            self.rect.centerx += self.boom_x
        if arg_kill:
            self.image.fill(self.color_int)
        if not arg_kill: #для главного тела яблока
            self.image.fill([255,0,0])
        if self.color_int.count(0) == 3:
            self.kill()
