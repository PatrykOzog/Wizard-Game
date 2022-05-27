import os
import sys
import pygame
from math import pi


class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(45, 45, 20, 20)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

    def vision(self):
        print("")


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)


# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
walls = []
player = Player()

level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W           W     W W   W   W         W W      W",
    "W W WWWW   WWWWWW W W W   W W WWW W W W W WWWW W",
    "W W W         W W       W   W W   W            W",
    "W W W W W  WWWW W WWW W WWW WWW W W WWWWWW  WW W",
    "W W W W       W   W   W W     W W W W       W  W",
    "WWW WWW  WW WWW WWW   WWW W W WWW W W WWWWW W  W",
    "W W W W   W     W W W                   W     WW",
    "W W W WW  WWW WWW W WWWWW W W W W WWW WWW  WW  W",
    "W     W   W W             W W W   W     W   W  W",
    "WWW   W WWW W   WW WW WWW WWW WWW WW    W W W  W",
    "W W   W W           W   W   W W         W W W  W",
    "W W W W W W W  WW WWW W W W WWWWW WW   WW W WW W",
    "W   W W     W   W W W W   W W     W       W    W",
    "W WWW W   W W WWW W WWWWW W WWW WWW W W W WWW  W",
    "W W W     W     W W   W W W   W     W   W W W  W",
    "W W WWWW WW W WWW W  WW WWWWWWW WWW WWW       WW",
    "W W W     W W             W W   W   W   W   W  W",
    "W W W WW WWWW   W WW WW W W W WWW WWW WWW   W  W",
    "W   W         W W W   W       W     W         WW",
    "W WWWWW W WWW W WWW WWW    WW WW WW W W W WWW  W",
    "W     W W W W     W W W     W     W W W W W    W",
    "WWW W   WWW W WW WW W WWWWW W WWW W WWWWW WWW WW",
    "W   W W   W           W     W W     W     W    W",
    "WWW W W WWW W WWW W   WWW W WWWWW  WWW WW W W  W",
    "W   W       W   W           W          T  W W  W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "T":
            end_rect = pygame.Rect(x, y, 20, 20)
        x += 40
    y += 40
    x = 0

running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.update()  # flip/update?
    clock.tick(360)

pygame.quit()
