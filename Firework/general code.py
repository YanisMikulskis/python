import pygame as pg
import sys
from window_size_salut import size_window
from zalp import ZALP
import random as rnd
pg.init()
#--------------------
screen = pg.display.set_mode(size_window())
pg.display.set_caption('HB to me')
fps = 144
clock = pg.time.Clock()
runGame = True
border = 0
#--------------------
alpha_value = 1
bloor_surf = pg.Surface(size_window())
#--------------------
red, green = [255,0,0], [0,255,0]
def rnd_colors():
    return [rnd.randint(1, 255) for _ in range(3)]
#--------------------
def make_volley(arg_X, arg_group):
    return ZALP(arg_X, size_window()[1], rnd_colors(), arg_group)

volley_group = pg.sprite.Group()
volley = make_volley(rnd.randint(0, size_window()[0]), volley_group)
#--------------------
BOOM_group = pg.sprite.Group()
def boom(arg_x, arg_y, color):
    var = rnd.random()
    [ZALP(arg_x, arg_y, color if var < 0.5 else rnd_colors(), BOOM_group) for _ in range(100)]
#--------------------
while runGame:
    bloor_surf.fill([0,0,0])
    screen.blit(bloor_surf, [0,0])
    bloor_surf.set_alpha(alpha_value)
    clock.tick(fps)
# --------------------
    cord_x_volley = rnd.randint(0, size_window()[0])

    volley_group.draw(screen)
    volley_group.update(0)

    volley_group_list = [_ for _ in volley_group]
    volley_group_list = volley_group_list[border:]
    if volley_group_list[-1].rect.y < rnd.randint(300, 600):
        make_volley(cord_x_volley, volley_group)
# --------------------
    for item in volley_group_list:
        if item.rect.y < rnd.randint(100, 300) and not item.boom_on_off:
            boom(item.rect.x, item.rect.y, rnd.choice([red, green]))
            item.boom_on_off = True
            border += volley_group_list.index(item)
            item.image.fill([0,0,0])
        if item.boom_on_off:
            BOOM_group.draw(screen)
            BOOM_group.update(1)
# --------------------
    [sys.exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.update()