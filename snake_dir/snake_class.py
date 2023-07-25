import pygame as pg
import random as rnd
from window_size_snake import size_window
import sys as SYS
segments_png = ['S1.png', 'S2.png', 'S3.png', 'S4.png', 'S5.png', 'S6.png', 'S7.png', 'TAIL.png']
class SNAKE(pg.sprite.Sprite):
    def __init__(self,x,y, filename, group, color_bool, head_snake, angle):
        pg.sprite.Sprite.__init__(self)
        self.filename = filename
        image_start = pg.image.load(self.filename).convert_alpha()
        #--------------------------------------------
        self.image_size = pg.transform.scale(image_start, [30, 30]).convert_alpha()
        self.angle = angle
        self.image = pg.transform.rotate(self.image_size, self.angle)
        self.rect = self.image.get_rect(center = [x, y])
        self.speed = 3
        self.speed_start = 3
        self.group = group
        self.add(self.group)
        self.freedrive = False
        self.VARROTHEAD= None
        self.VAR = True
        # ^атрибут для разворота сегментов. введен для того,
        # чтобы определять зависимость элемента с предыдущим до выполнения условия с координатами.
        # после этого условия происходит разворот сегмента
        # ------------------------------------------
        if head_snake: self.arr, self.map_rotates = [], []#список-след движения головы(коллекция координат)
                                                                                                # и карта поворотов головы
        #метод ниже используется только для головы! именно действия. все остальное заходит в параметры
    def update(self,snake_segments, vector, scale_arg, next_cords=0):
      
        if scale_arg % 5 == 0 and scale_arg != 0: #условие для увеличения скорости каждые 5 очков
            self.speed = self.speed_start + scale_arg//5
        # ------------------------------------------
        def Foo_ROTATE(angle):
            #функция для разворот головы змеи (в парамтерах функции угол разворота) с минусом он идет по часовой
            #стрелке. без минуса - против. в функции еще в список вносится угол для поворотов сегментов
            self.image = pg.transform.rotate(self.image, angle)
            self.map_rotates.append(angle)
            return self.image
        match vector:
            #движение для первого элемента(головы) и разворот в пространстве в зависимости от ее положения.
            # угол поворота зависит от отношения координат (х или у) центров головы и первого сегмента
            case 'up':
                self.rect.centery -= self.speed
                if self.VARROTHEAD != 'up':
                    self.VARROTHEAD = 'up'
                    if self.rect.centerx < snake_segments[1].rect.centerx: Foo_ROTATE(-90)
                    elif self.rect.centerx > snake_segments[1].rect.centerx: Foo_ROTATE(-270)
                    elif self.rect.centery > snake_segments[1].rect.centery: Foo_ROTATE(180)
            case 'left':
                self.rect.centerx -= self.speed
                if self.VARROTHEAD != 'left':
                    self.VARROTHEAD = 'left'
                    if self.rect.centery < snake_segments[1].rect.centery: Foo_ROTATE(90)
                    elif self.rect.centery > snake_segments[1].rect.centery: Foo_ROTATE(-90)
                    elif self.rect.centerx > snake_segments[1].rect.centerx: Foo_ROTATE(180)
            case 'right':
                self.rect.centerx += self.speed
                if self.VARROTHEAD != 'right':
                    self.VARROTHEAD = 'right'
                    if self.rect.centery < snake_segments[1].rect.centery: Foo_ROTATE(-90)
                    elif self.rect.centery > snake_segments[1].rect.centery: Foo_ROTATE(90)
                    elif self.rect.centerx < snake_segments[1].rect.centerx: Foo_ROTATE(180)
            case 'down':
                self.rect.centery += self.speed
                if self.VARROTHEAD != 'down':
                    self.VARROTHEAD = 'down'
                    if self.rect.centerx < snake_segments[1].rect.centerx: Foo_ROTATE(90)
                    elif self.rect.centerx > snake_segments[1].rect.centerx: Foo_ROTATE(-90)
                    elif self.rect.centery > snake_segments[1].rect.centery: Foo_ROTATE(180)
        # ------------------------------------------
        self.arr.append(list(snake_segments[0].rect.center)) #список координат (след), который прошел первый элемент (голова)
        self.map_rotates.append(0) #список углов поворота головы змеи. когда поворота нет в список записывается 0
        # ------------------------------------------
        for i in snake_segments[1:]:
            #движение для последующих частей. каждая часть идет по пути(следу) головы змейки.
                                    #при добавлении нового сегмента, к последнему элементу следа добавляется длина
                                    # сегмента умноженная на его индекс в списке сегментов (snake_segments).получившееся число -
                                    #это индекс списка-следа, на который садится новый сегмент. и так все движение
                                    #движется первый элемента а за ним другие элементы в соответствии с длиной
                                    # и их порядковым номером в списке сегментов
        #-----------------------------------------
            if not self.freedrive: #условие только для первого после головы элемента
                if i.rect.centerx > self.arr[-1][0]:
                    i.rect.centerx -= self.speed
            if snake_segments[-1].rect.centerx <= self.arr[0][0]:
                #условие только для первого после головы элемента.все это нужно чтобы сегмент
                # с индексом 1 начал движение по следу, так как в начале он не попадает в след
                self.freedrive = True
        # -----------------------------------------
            if self.freedrive:#начало движения по следу. код выше для первого после головы элемента уже не нужен
                i.rect.center = self.arr[-self.image.get_width() // self.speed * snake_segments.index(i)]
                 #движение по следу. центр каждого элемента находится друг от друга на расстоянии длины каждого элемента
                #на скорость УМНОЖАЕМ ИНДЕКС (не делим длину элемента на нее!),
                # чтобы можно было ее менять и не использовать только self.speed = 1
        # -----------------------------------------
                i.image = pg.transform.rotate(i.image, self.map_rotates[-self.image.get_width() //
                                                                        self.speed * snake_segments.index(i)])
                #теперь к поворотам. список self.map_rotates - это своего рода карта поворотов головы змеи.
                #по умолчанию в нее записывается 0. при поворотах в эту карту записывается угол, которые подается
                #параметром в функцию Foo_ROTATE.и также как при движении,
                # сегменты идут по этой карте и поворачивают в соответсвующих местах.их угол равен элементу списка с индексом
                # [отрицательной длины элемента деленной на скорость и помноженной на индекс сегмента в списке сегментов]
        # -----------------------------------------
                if len(snake_segments[1:]) >= 4:
                    if len(self.arr[:-self.image.get_width()*len(snake_segments[1:])]) >= self.image.get_width()*2:
                            del self.arr[0]
                    if len(self.map_rotates[:-self.image.get_width()* len(snake_segments[1:])]) >= self.image.get_width()*2:
                        del self.map_rotates[0]
                #если длина змеи (не считая головы) больше 4 сегментов и если длина куска списка-следа
                # от его начала до последнего сегмента змеи(по индексу в списке-следе) больше удвоенного значения длины змеи,
                # то удаляем первый элемен в списке-следе. таким образом, настанет момент, когда у нас расстояние от начала
                #списка-следа до последнего элемента не будет превышать расстояние двух сегментов и список
                # будет расти очень медленно.задача по избавлению от быстрого роста списка-следа выполнена.
                #для карты поворотов делаем тоже самое
            next_cords += 1
        # ------------------------------------------
        # условие, если змея заползет за границы окна
        if snake_segments[0].rect.centerx > size_window()[0] or snake_segments[0].rect.centerx < 0:
            SYS.exit()
        elif snake_segments[0].rect.centery > size_window()[1] or snake_segments[0].rect.centery < 0:
            print(f'Игра окончена!')
            SYS.exit()



