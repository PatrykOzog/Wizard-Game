import os
import sys
import pygame
import math


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("wizard1.png").convert_alpha()
        self.wall_image = pygame.image.load("floor1.png").convert_alpha()
        self.treasure_image = pygame.image.load("Treasure.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(1850, 1000))
        self.rot_image = self.player_image
        self.rot_image_rect = self.player_rect
        self.offset = pygame.math.Vector2()

    def move(self, dx, dy):
        enemy.enemy_rect.x -= dx
        enemy.enemy_rect.y -= dy
        self.offset.x -= dx
        self.offset.y -= dy
        for wall in walls:
            wall.wall_rect.x -= dx
            wall.wall_rect.y -= dy
            if self.player_rect.colliderect(wall.wall_rect):
                if dx != 0:
                    for wall in walls:
                        wall.wall_rect.x += dx
                if dy != 0:
                    for wall in walls:
                        wall.wall_rect.y += dy


    def rotate(self):
        mx, my = pygame.mouse.get_pos()
        ddx, ddy = mx - self.player_rect.centerx, my - self.player_rect.centery
        self.angle = math.degrees(math.atan2(-ddy, ddx)) - 90
        self.rot_image = pygame.transform.rotate(self.player_image, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center=self.player_rect.center)

    def cast_rays(self):
        start_angle = math.radians(self.angle) - math.pi/6
        for ray in range(5):
            for depth in range(200):
                target_x = self.player_rect.centerx - math.sin(start_angle) * depth
                target_y = self.player_rect.centery - math.cos(start_angle) * depth
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                for wall in walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        #pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                        break
                    #else:
                        #pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break

            start_angle += math.pi / 15


class Wall(object):

    def __init__(self, pos):
        walls.append(self)
        self.wall_rect = pygame.Rect(pos[0], pos[1], 40, 40)


class Enemy(object):

    def __init__(self):
        self.enemy_rect = pygame.Rect(1000, 850, 20, 20)


# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get the treasure!")
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
walls = []
player = Player()
enemy = Enemy()

level = (
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    "W           W     W W   W   W         W W      W"
    "W W WWWW   WWWWWW W W W   W W WWW W W W W WWWW W"
    "W W W         W W       W   W W   W            W"
    "W W W W W  WWWW W WWW W WWW WWW W W WWWWWW  WW W"
    "W W W W       W   W   W W     W W W W       W  W"
    "WWW WWW  WW WWW WWW   WWW W W WWW W W WWWWW W  W"
    "W W W W   W     W W W                   W     WW"
    "W W W WW  WWW WWW W WWWWW W W W W WWW WWW  WW  W"
    "W     W   W W             W W W   W     W   W  W"
    "WWW   W WWW W   WW WW WWW WWW WWW WW    W W W  W"
    "W W   W W           W   W   W W         W W W  W"
    "W W W W W W W  WW WWW W W W WWWWW WW   WW W WW W"
    "W   W W     W   W W W W   W W     W       W    W"
    "W WWW W   W W WWW W WWWWW W WWW WWW W W W WWW  W"
    "W W W     W     W W   W W W   W     W   W W W  W"
    "W W WWWW WW W WWW W  WW WWWWWWW WWW WWW       WW"
    "W W W     W W             W W   W   W   W   W  W"
    "W W W WW WWWW   W WW WW W W W WWW WWW WWW   W  W"
    "W   W         W W W   W       W     W         WW"
    "W WWWWW W WWW W WWW WWW    WW WW WW W W W WWW  W"
    "W     W W W W     W W W     W     W W W W W    W"
    "WWW W   WWW W WW WW W WWWWW W WWW W WWWWW WWW WW"
    "W   W W   W           W     W W     W     W    W"
    "WWW W W WWW W WWW W   WWW W WWWWW  WWW WW W W  W"
    "W   W       W   W           W          T  W W  W"
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
)

x = y = 0
for rows in range(27):
    for columns in range(48):
        square = rows*48+columns
        if level[square] == "W":
            Wall((x, y))
        if level[square] == "T":
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
        screen.blit(player.wall_image, wall.wall_rect)
    screen.blit(player.treasure_image, end_rect)
    screen.blit(player.rot_image, player.rot_image_rect)
    player.rotate()
    player.cast_rays()
    wol1 = pygame.Rect(100, 100, 50, 50)
    wol2 = pygame.Rect(200, 200, 20, 20)
    wol = pygame.Rect.union(wol1, wol2)
    pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect)
    pygame.display.update()  # flip/update?
    clock.tick(360)

pygame.quit()
