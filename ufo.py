import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
from bullet import BulletFromAlien
from random import randint

class UFOs:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.game = game

        self.ufo_group = Group()
        self.last_ufo = pg.time.get_ticks()

    def create_ufo_if_time(self):
        now = pg.time.get_ticks()
        if now > self.last_ufo + self.settings.ufo_every * 1000:
            self.ufo_group.add(UFO(game=self.game, parent=self))
            self.last_ufo = pg.time.get_ticks()

    def update(self):
        self.create_ufo_if_time()
        self.ufo_group.update()
        for ufo in self.ufo_group.sprites():
            ufo.draw()
            if ufo.check_edges():
                self.ufo_group.remove(ufo)

        bullet_ufo_collision = pg.sprite.groupcollide(self.ufo_group, self.game.ship.bullet_group_that_kill_aliens,
                                                      True, True)
        if bullet_ufo_collision:
            for ufo in bullet_ufo_collision:
                print('UFO HIT')
                ufo.killed()


    def draw(self):
        for ufo in self.ufo_group:
            ufo.draw()


class UFO(Sprite):

    def __init__(self, game, parent):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.game = game
        self.parent = parent
        self.image = pg.image.load('images/UFO.png')
        self.pointImage = pg.image.load('images/250.png')
        self.rect = self.image.get_rect()
        self.center = 0

        self.dead = self.timeDead = self.reallydead = False
        self.timer_switched = False
        self.timer = None

        # self.points = randint(100, 500)
        self.points = 250

    def check_edges(self):
        rscreen = self.screen.get_rect()
        return self.rect.left > rscreen.right

    def update(self):
        if not self.dead:
            delta = self.settings.alien_speed + 1
            self.rect.x += delta
        if self.dead and pg.time.get_ticks() < self.timeDead + 600:
            self.image = self.pointImage
        else:
            self.reallydead = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def killed(self):
        if not self.dead and not self.reallydead:
            self.dead = True
            self.timeDead = pg.time.get_ticks()
            self.game.stats.score += self.settings.alien_points * len(self.parent.alien_group)
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()
            self.parent.remove(self)