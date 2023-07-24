import pygame as pg
import random as rnd
import sys
from window_size import size_window
from letters2 import LETTER
import time
pg.init()
#-----Создание окна
SCREEN = pg.display.set_mode(size_window())
pg.display.set_caption('MATRIX')
#--------------Переменные окна
clock = pg.time.Clock()
FPS = 60
runGame = True
white = [255, 255, 255]
green = [0, 255, 0]
RED = [255,0,0]
alpha_value = 0 #альфа канал для размытия
bloor_surf = pg.Surface(size_window()) #поверхность на окне для размытия
#--------------------------
# алфавит Катакана (из Матрицы) и параметры шрифта. Создаем большой список из катаканских букв и других символов
katakana = [chr(j) for j in range(int('0x30a0', 16), (int('0x30a0', 16) + 96))]
numbers = [str(i) for i in range(10)]
flags = ['-', '+', '=', '!', '&', '?', '<', '>', '@']
general_list = katakana + numbers + flags
letter_style_FOR_INFO = ('pingfang', 48)
#--------------------------
#список стартовых ОТРИЦАТЕЛЬНЫХ координат по оси У(буквы должны появляться ВНЕ экрана) и координат по оси Х, которые
#количество которых идет в зависимости от длины окна с шагом 50. Окно у нас создается через импортируемую функцию size_window()
letters_y, letters_x = [-i for i in range(0, 660, 22)], [j for j in range(25, size_window()[0], 50)]
letters_x_BG = [l for l in range(10, size_window()[0], 10)]
#--------------------------
#функция создания ОДНОЙ буквы.создаем экземпляр класса LETTER и накидываем атрибуты
def create_letter(par_x, par_y, par_let, par_color, par_group, par_speed, par_WS):
    letter_matrix = LETTER(par_x, par_y, par_let, par_color, par_group, par_speed, par_WS)
    return letter_matrix
#--------------------------
#Списки, в которые будут закидываться группы: список групп основных символов и список групп фоновых символов
groups = []
groups_bg = []
#--------------------------
#функция создания ОДНОЙ колонны по которой будут бежать столбцы
def make_column(arg_color, x_arg, speed_arg, arg_group, arg_WS):
    size_column = letters_y[rnd.randint(1, 5):rnd.randint(6, len(letters_y))]

    for symbol in size_column:
        create_letter(x_arg, symbol, rnd.choice(general_list), arg_color, arg_group, speed_arg, arg_WS)
    return True
#--------------------------
#цикл создания колонн основных символов и фоновых в соответствии со списком координат по х
for column in letters_x:
    speed_letters = rnd.randint(3, 6)#скорость одной колонны
    let_group = pg.sprite.Group()#группа одной колонны
    make_column([0,255,0], column, speed_letters, let_group, 24)#создание колонны
    groups.append(let_group)#добавление группы в список групп
    #ниже тоже самое для фоновых символов, только мы будем их чуток отклонять от основной координаты х
    speed_BG = rnd.randint(3,6)
    let_group_BG = pg.sprite.Group()
    make_column([0, 40, 0], column + rnd.randint(-30, 30), speed_BG, let_group_BG, 16)
    groups_bg.append(let_group_BG)
#--------------------------
#Основной цикл анимации
while runGame:
    bloor_surf.fill([0,0,0])
    clock.tick(FPS)
    # --------------------------
    #Нижние две строки для небольшого развития
    SCREEN.blit(bloor_surf, [0, 0])
    bloor_surf.set_alpha(alpha_value)
    # --------------------------
    #цикл по спискам групп и применение к ним функции draw() для размещения и метода update для остального(см.в классе)
    #для основных символов
    [i.draw(SCREEN) for i in groups]
    [i.update() for i in groups]
    # для фоновых символов
    [i.draw(SCREEN) for i in groups_bg]
    [i.update() for i in groups_bg]
    # --------------------------
    #циклы для появления следующих столбцов в колонне. Объяснение: когда коорд. Y последнего символа в списке
    # (созданном из группы item в списке групп groups на текущей итерации цикла) становится равна случайному значению от
    # 100 до 300, то мы создаем новый столбец с [цвет, коорд.х последнего символа, скорость посл. символа, текущая группа,
    #шрифт]. В текущую группу мы закидываем символ для того, чтобы она постоянно обновлялась и последний элемент менялся.
    #иначе у нас происходит единое выполнение условия и элементы начинают появляться бесконтрольно
    for item in groups:
        group_list = [elem for elem in item]
        if group_list[-1].rect.y > rnd.randint(100, 300):
            make_column([0, 255, 0], group_list[-1].x, group_list[-1].speed, item, 24)
    #для фоновых колонн тоже самое с той лишь разницей, что цвет будет случайным из диапазона зеленых цветов (от
    #тусклого к яркому) и через словарь мы создаем пары (шрифт, цвет), т.е. чем меньше шрифт, тем тусклее цвет. Можно
    #сделать и наоборот, без разницы. И кидаем их в функцию make_column()
    for elem in groups_bg:
        groups_bg_list = [item for item in elem]
    #------через словарь
        # GD = {
        #
        # }
        # for i in groups_bg_list:
        #     GD.setdefault(groups_bg_list.index(i), i)
        # print(GD)
        # if GD.get(len(GD) - 1).rect.y > rnd.randint(100, 300):
        #     word_size = rnd.choice([4, 6, 8, 10, 12, 14, 16, 18, 20])
        #     make_column([0, 255, 0], groups_bg_list[-1].rect.x + rnd.randint(-30, 30), groups_bg_list[-1].speed, elem,
        #                 word_size)
        if groups_bg_list[-1].rect.y > rnd.randint(100, 300):
            word_sizes = [i*2 for i in range(7)][1:]
            colors_bg = [[0, i + 20, 0] for i in range(0, 140, 20)]
            bg_params_dict = {
                                }
            for i in zip(word_sizes, colors_bg):
                bg_params_dict.setdefault(i[0], i[1])
            current_size = rnd.choice(word_sizes)
            make_column(bg_params_dict.get(current_size), groups_bg_list[-1].rect.x + rnd.randint(-30, 30), groups_bg_list[-1].speed, elem, current_size)
    # --------------------------
    #постепенное уменьшение размытие с ходом анимации
    alpha_value = alpha_value + 1 if alpha_value < 100 else 100
    # --------------------------
    [sys.exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.update()




