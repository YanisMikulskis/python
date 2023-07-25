import pygame as pg
import sys
import random as rnd
from window_size_snake import size_window
from snake_class import SNAKE
from apple import APPLE
#------------------------------------------
pg.init()
#------------------------------------------
#создание окна
screen = pg.display.set_mode(size_window())
pg.display.set_caption('SNAKE')
fps = 144
clock = pg.time.Clock()
runGame = True
#------------------------------------------
#переменные для движения
left,right,up,down = pg.K_a, pg.K_d, pg.K_w, pg.K_s
motion = None
#------------------------------------------
#переменные цвета
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
random_color = [rnd.randint(1, 255) for i in range(3)]
#------------------------------------------
#Создание групп для тела змеи и спор яблока
snake_G, apple_G = pg.sprite.Group(), pg.sprite.Group()
#------------------------------------------
#переменные для взрыва
boom_var = False
apples_boom = []
#------------------------------------------
#экземпляр класса первого элемента змеи(головы),переменные для него и картинки для сегментов
x_snake, y_snake = 500, 500
snake = SNAKE(x_snake, y_snake, 'HEAD.png', snake_G, True, True, 90)
segments_png = ['S1.png', 'S2.png', 'S3.png', 'S4.png', 'S5.png', 'S6.png', 'S7.png', 'TAIL.png']
SPEED_LR, SPEED_UD = snake.image.get_width(), snake.image.get_height()
#------------------------------------------

#функции, создающие координаты яблок. так удобнее
def make_x(): return rnd.randint(1, 900)
def make_y(): return rnd.randint(1, 900)
#------------------------------------------
#экзепляр класса тела яблока
apple_body = APPLE(x=make_x(), y=make_y(), filename='OB_SNAKE.png', size=[5,5],group=None, color_yellow=False)
#------------------------------------------
#функция создания остальных сегментов. создаем один ВНЕ цикла, чтобы было два первых сегм.
def make_snake(x_snake_arg, y_snake_arg, SG_ARG, angle):
    if SG_ARG:
        if SG_ARG[-1].rect.centerx < SG_ARG[-2].rect.centerx:
            angle = -90
        elif SG_ARG[-1].rect.centerx > SG_ARG[-2].rect.centerx:
            angle = 90
        elif SG_ARG[-1].rect.centery > SG_ARG[-2].rect.centery:
            angle = 0
        elif SG_ARG[-1].rect.centery < SG_ARG[-2].rect.centery:
            angle = 180
        SG_ARG[-1].kill()

    snake_s = SNAKE(x_snake_arg,y_snake_arg, rnd.choice(segments_png[:-1]), snake_G, False, False, angle)
    if SG_ARG: make_tail(SG_ARG, angle)
    #в функции создания нового сегмента будем вызывать функцию создания хвоста( она ниже). причем два раза условие
    # if SG_ARG мы пишем для того, чтобы создался второй сегмент так как в нем мы передаем значение None в этот параметр
    #если у нас все будет в одном словии то змея у нас будет иметь изначально только хвост и голову. а нам нужен элемент
    #как создается хвост: при столкновении с яблоком вызывается эта функция. выбирается по условию угол, затем уничтожается
    # хвост.на его место встает сегмент (snake_s) а потом втсавляется хвост. используется параметр, который является списком из группы
    #он подается в функцию создания хвоста. и получаем хвост
    return snake_s
make_snake(snake.rect.centerx + snake.image.get_width(), y_snake, None, 90)
#для того, что сегмент при появлении был повернут в нужную сторону(в сторону движения змеи), мы в функцию добавим условие
#1) отношение координат (х или у) последнего сегмента к предпоследнему
#2) угол поворота, который мы будем отправлять в атрибуты класса Змеи. этот угол будет зависеть от отношения координат сегментов,
# которые мы берем из списка всех элементов змеи (SG_ARG).при создании второго элемента мы на это место отправляем None,
# так как в этот момент нужный список еще не создан
#------------------------------------------
#функция создания хвоста и специальная переменная, чтобы он создавался в начале один раз
tail_on = True
def make_tail(SG_ARG, angle_for_tail):
    tail = SNAKE(SG_ARG[-1].rect.centerx + SG_ARG[-1].image.get_width(), y_snake, 'TAIL.png', snake_G,
            True, True, angle_for_tail)
    #нужно будет в перспективе откалибровать хвост чтобы он всегда поворачивал куда надо
#------------------------------------------
#функция создания спор вокруг яблока
def apple_spore(arg_x, arg_y, arg_color):
    arg_x += rnd.randint(-10, 10)
    arg_y += rnd.randint(-10, 10)
    return APPLE(arg_x, arg_y, 'STAR.png', [2,2],apple_G, arg_color)
#------------------------------------------
#начальные переменные для счета
SCALE_NUM = 0
scale_x, scale_y = size_window()[0] - size_window()[0]/3.5, size_window()[1] - size_window()[1]//10
letter_style_FOR_SCALE = ('applegothic', 48)
#начальные данные для других надписей
letter_style_FOR_INFO = ('applegothic', 48)
#переменная для фона
background_start = pg.image.load('BG.jpg').convert_alpha()
background = pg.transform.scale(background_start, [1200, 1000])
#переменная для прозрачности надписи о скорости
transparency = 255
var_tran = False
#------------------------------------------
# def make_speed_font(arg_color):
#     scale_SURFACE = pg.font.SysFont(*letter_style_FOR_SCALE).render(f'Счет: {SCALE_NUM}', True, [0, 0, 255])
#     scale_RECT = scale_SURFACE.get_rect(topleft=[scale_x, scale_y])
while runGame:
    screen.blit(background, [0,0])
    clock.tick(fps)
    keys = pg.key.get_pressed()
    # ------------------------------------------
    # rect для счета.создаем его в цикле для того, чтобы динамически могло меняться расположение
    scale_SURFACE = pg.font.SysFont(*letter_style_FOR_SCALE).render(f'Счет: {SCALE_NUM}', True, [0, 0, 255])
    scale_RECT = scale_SURFACE.get_rect(topleft=[scale_x, scale_y])
    # ------------------------------------------
    #Дополнительные надписи(может в последствии изменяться)
    if transparency <= 0: transparency = 0
    speed_info = pg.font.SysFont(*letter_style_FOR_INFO).render(f'Скорость увеличена', True, [0, 0, 255])
    speed_info_RECT = speed_info.get_rect(topleft=[75,0])
    speed_info.set_alpha(transparency) #прозрачность надписи
    # ------------------------------------------
    snake_parts_l = [i for i in snake_G]#список из элементов группы (для удобства)
    #^изначальное положение (поворот) нового элемента при его появлении(когда змея съедает яблоко)
    snake_parts_l_x = [i.rect.centerx for i in snake_parts_l]  # список всех координат "х" у списка(т.е) группы частей змеи
    snake_parts_l_y = [i.rect.centery for i in snake_parts_l]  # список всех координат "у" у списка(т.е) группы частей змеи
    # ------------------------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN:
            match event.key:
                    case pg.K_w: motion = 'UP'
                    case pg.K_a: motion = 'LEFT'
                    case pg.K_s: motion = 'DOWN'
                    case pg.K_d: motion = 'RIGHT'
    match motion:
        case 'UP': snake.update(snake_parts_l, 'up',SCALE_NUM)
        case 'LEFT':snake.update(snake_parts_l, 'left', SCALE_NUM)
        case 'DOWN': snake.update(snake_parts_l, 'down', SCALE_NUM)
        case 'RIGHT': snake.update(snake_parts_l, 'right', SCALE_NUM)
    # ------------------------------------------
    if apple_body.rect.colliderect(snake_parts_l[0].rect): #столкновение с яблоком
        boom_var = True
        SCALE_NUM += 1
        if SCALE_NUM % 5 == 0 and SCALE_NUM != 0:
            var_tran = True #условие для записи true в переменную-крючок var_tran.опираясь на нее,
            # будет появляться надпись и постепенно гаснуть
        for i in apple_G:
            apples_boom.append(i) #спрайты пыльцы во время столкновения из групп переносятся в пустой
                                #список и переменная boom_var становится равна True. и когда она становится этому равна
                                # метод update(1,1)(вместе со взрывом) срабатывает на элементы этого списка
        del apple_body #удаление тела яблока
        apple_body = APPLE(make_x(), make_y(), 'OB_SNAKE.png', [5, 5], None, True)#удаление тела яблока и создание нового
        # ------------------------------------------
        #добавление сегмента в змею.конкретное место добавления сегмента
        # определяется в классе змеи когда она идет по пути self.arr.изначально сегмент добавляется всегда
        # правее предыдущего сегмента(так как изначально эта операция делалась
        # при цсловии что появляться он бужет именно справа).но мы этого не видим так как он моментально встает
        # на свое место благодаря движению по пути self.arr
        if snake_parts_l[-1].rect.centery == snake_parts_l[-2].rect.centery:
            x_snake_new = snake_parts_l[-1].rect.centerx + snake.image.get_width()
            make_snake(x_snake_new, snake_parts_l[-1].rect.centery, snake_parts_l, None)
        if snake_parts_l[-1].rect.centerx == snake_parts_l[-2].rect.centerx:
            y_snake_new = snake_parts_l[-1].rect.centery + snake.image.get_height()
            make_snake(snake_parts_l[-1].rect.centerx, y_snake_new, snake_parts_l, None)
    # ------------------------------------------
    else:#когда змея не сталкивается создаем непрерывно споры вокруг яблока
        for i in range(2):
            apple_spore(apple_body.rect.centerx, apple_body.rect.centery, arg_color=True)
    # ------------------------------------------
    if tail_on:
        make_tail(SG_ARG=snake_parts_l, angle_for_tail=90) #начальный угол равен 90
        tail_on = False
    # ------------------------------------------
    for i in snake_parts_l[5:]: #проверка на пересечение змеи самой себя
        if snake_parts_l[0].rect.colliderect(i.rect):
            sys.exit()
    # ------------------------------------------
    if boom_var: #взрыв при столкновении с яблоком
        for i in apples_boom:
            i.image = pg.transform.scale(i.image, [3,3])
            i.update(1,True)
            if i.rect.centery > size_window()[1]:
                apples_boom.pop(apples_boom.index(i))
        if len(apples_boom) == 0:
            boom_var = False
    #-------------------------------------------
    apple_G.draw(screen)
    apple_G.update(0, True)
    # ------------------------------------------
    screen.blit(apple_body.image, apple_body.rect)
    apple_body.update(0, False)
    # ------------------------------------------
    snake_G.draw(screen)
    # ------------------------------------------
    #если правая граница счета (объекта rect для него) заходит за границу экран, то этот объект двигается влево
    screen.blit(scale_SURFACE, scale_RECT)
    if scale_RECT.right > size_window()[0]:
        scale_x -= scale_RECT.right - size_window()[0]
    # ------------------------------------------
    #Код для мигающей надписи. Каждый пять очков окгда скорость увеличивается - появляется надпись,
    # которая постепенно исчезает
    if transparency == 0:
        var_tran = False
        transparency = 255
    if var_tran:
        transparency -= 1
        screen.blit(speed_info, speed_info_RECT)
    # ------------------------------------------
    pg.display.update()