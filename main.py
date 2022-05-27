import os
import sys
import pygame
import math


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("Player.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(60, 60))
        self.rot_image = self.player_image
        self.rot_image_rect = self.player_rect
        # self.rect = pygame.Rect(45, 45, 20, 20)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.player_rect.x += dx
        self.player_rect.y += dy

        for wall in walls:
            if self.player_rect.colliderect(wall.rect):
                if dx > 0:
                    self.player_rect.right = wall.rect.left
                if dx < 0:
                    self.player_rect.left = wall.rect.right
                if dy > 0:
                    self.player_rect.bottom = wall.rect.top
                if dy < 0:
                    self.player_rect.top = wall.rect.bottom

    def rotate(self):
        mx, my = pygame.mouse.get_pos()
        ddx, ddy = mx - self.player_rect.centerx, my - self.player_rect.centery
        angle = math.degrees(math.atan2(-ddy, ddx)) - 90
        self.rot_image = pygame.transform.rotate(self.player_image, angle)
        self.rot_image_rect = self.rot_image.get_rect(center=self.player_rect.center)


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)


# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get the treasure!")
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

icon = pygame.image.load("agent.png")
pygame.display.set_icon(icon)

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

    if player.player_rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    screen.blit(player.rot_image, player.rot_image_rect)
    player.rotate()
    pygame.display.update()  # flip/update?
    clock.tick(360)

pygame.quit()
