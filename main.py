import sys, pygame
from math import cos, pi, sin, sqrt
from random import randint

size = width, height = 640, 480  # Размеры экрана
black = 0, 0, 0  # rgb черного цвета


class Ball(object):
    def __init__(self, x, y):
        self.speed = [randint(-2, 2), randint(-2, 2)]
        self.ball = pygame.image.load("basketball.png")
        self.ballrect = self.ball.get_rect()
        self.ballrect.top = y
        self.ballrect.left = x

    def set_pos(self, pos):
        self.ballrect.left = pos[0] - self.ballrect.width // 2
        self.ballrect.top = pos[1] - self.ballrect.height // 2

    def shift(self):
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > width:
            self.speed[0] *= -1
        if self.ballrect.top < 0 or self.ballrect.bottom > height:
            self.speed[1] *= -1

    def collides_with_simple(self, other):
        x1 = self.ballrect.centerx
        y1 = self.ballrect.centery
        x2 = other.ballrect.centerx
        y2 = other.ballrect.centery
        r = sqrt((x1-x2)**2 + (y1-y2)**2)
        return r<self.ballrect.width

    def collides_with(self, other):
        return self.ballrect.colliderect(other.ballrect)

    def bounce(self):               # stupid algo
        self.speed[0] *= -1
        self.speed[1] *= -1

    def bounce_with(self, b):       # just simple swap vectors
        self.speed, b.speed = b.speed, self.speed


def init_with_positions():
    b = [None] * 5
    for i in range(5):
        x = width // 2 + 150*cos(2*pi/5*i)
        y = height // 2 + 150*sin(2*pi/5*i)
        b[i] = Ball(x, y)
    return b


def check_collisions(b):
    for i in range(5):
        for j in range(i + 1, 5):
            if b[i].collides_with_simple(b[j]):
                print("Collision: {} - {}".format(i, j))
                b[i].bounce_with(b[j])
                # b[i].bounce()
                # b[j].bounce()


def main():
    global size, width, height
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
    b = init_with_positions()
    gameover = False
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                gameover = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        for i in range(5): b[i].shift()
        check_collisions(b)
        screen.fill(black)
        for i in range(5): screen.blit(b[i].ball, b[i].ballrect)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


main()
