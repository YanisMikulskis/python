import pygame as pg
import random
from window_size_salut import size_window

class ZALP(pg.sprite.Sprite):
    def __init__(self, x, y, color, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([1, 3])
        self.rect = self.image.get_rect(topleft=[x,y])
        self.color = color
        self.image.fill(self.color)
        self.add(group)
        self.speed_boom_x, self.speed_boom_Y = \
            random.randint(-10,10), random.randint(-10,10)
        self.boom_on_off = False
        self.speed = 3
    def update(self,boom):
        if boom:
            self.rect.y += self.speed_boom_Y
            self.rect.x += self.speed_boom_x
            if self.speed_boom_x > 0 and self.speed_boom_Y < 0:
                self.speed_boom_x -= 0.5
                self.speed_boom_Y += 0.5
            elif self.speed_boom_x >= 0 and self.speed_boom_Y >= 0:
                self.speed_boom_Y += 0.5
            elif self.speed_boom_x <= 0 and self.speed_boom_Y <= 0:
                self.speed_boom_x += 0.5
                self.speed_boom_Y += 0.5
            elif self.speed_boom_x <= 0 and self.speed_boom_Y >= 0:
                self.speed_boom_Y += 0.5
            if self.rect.x < 0 or self.rect.x > size_window()[0]: self.kill()
            if self.rect.y < 0 or self.rect.y > size_window()[1]: self.kill()
        else:
            self.rect.y -= self.speed






