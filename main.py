import os
import sys
import pygame
import pygame.gfxdraw
import math


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("wizard1.png").convert_alpha()
        self.wall_image = pygame.image.load("floor1.png").convert_alpha()
        self.treasure_image = pygame.image.load("Treasure.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(480, 270))
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
        points = []
        starting_point = ((self.player_rect.centerx, self.player_rect.centery))
        start_angle = math.radians(self.angle) - math.pi/6
        for ray in range(50):
            for depth in range(50):
                target_x = self.player_rect.centerx - math.sin(start_angle) * depth * 5
                target_y = self.player_rect.centery - math.cos(start_angle) * depth * 5
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                for wall in walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        #pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                        points.append((target_x, target_y))
                        screen.blit(player.wall_image, wall.wall_rect)
                        break
                    #else:
                        #pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break
            points.append((target_x, target_y))
            start_angle += math.pi / 150

        for point in points:
            pygame.gfxdraw.filled_polygon(screen, (point, starting_point, self.player_rect.center), (255, 255, 100))
            starting_point = point
            #pygame.draw.circle(screen, (0, 255, 255), point, 5)

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
points = []
player = Player()
enemy = Enemy()

level = (
    "WWWWWWWWWWWWWWWWWWWW"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W        WW        W"
    "W        WW        W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W                  W"
    "W          T       W"
    "W                  W"
    "WWWWWWWWWWWWWWWWWWWW"
)

x = y = 0
for rows in range(20):
    for columns in range(20):
        square = rows*20+columns
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

    screen.fill((25, 25, 25))
    player.wall_image.set_alpha(50)
    for wall in walls:
        screen.blit(player.wall_image, wall.wall_rect)
    screen.blit(player.treasure_image, end_rect)
    screen.blit(player.rot_image, player.rot_image_rect)
    player.rotate()
    player.cast_rays()
    pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect)
    pygame.display.flip()  # flip/update?
    clock.tick(360)

pygame.quit()