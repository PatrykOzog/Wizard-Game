import os
import sys
import pygame
import pygame.gfxdraw
import math
import random


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("wizard1.png").convert_alpha()
        self.treasure_image = pygame.image.load("Treasure.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(480, 270))
        self.rot_image = self.player_image
        self.rot_image_rect = self.player_rect

    def move(self, dx, dy):
        for enemy in enemies:
            enemy.enemy_rect.x -= dx
            enemy.enemy_rect.y -= dy
        for wall in walls:
            wall.wall_rect.x -= dx
            wall.wall_rect.y -= dy
            if self.player_rect.colliderect(wall.wall_rect):
                for enemy in enemies:
                    enemy.enemy_rect.x += dx
                    enemy.enemy_rect.y += dy
                for wall in walls:
                    wall.wall_rect.x += dx
                    wall.wall_rect.y += dy

    def rotate(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.player_rect.centerx, my - self.player_rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.rot_image = pygame.transform.rotate(self.player_image, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center=self.player_rect.center)

    def cast_rays(self):
        points = []
        starting_point = (self.player_rect.centerx, self.player_rect.centery)
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
                        screen.blit(wall.wall_image, wall.wall_rect)
                        break
                else:
                    continue
                break
            points.append((target_x, target_y))
            start_angle += math.pi / 150

        for point in points:
            pygame.gfxdraw.filled_polygon(screen, (point, starting_point, self.player_rect.center), (255, 255, 100, 70))
            starting_point = point
            #pygame.draw.circle(screen, (0, 255, 255), point, 5)
            #screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

    def player_update(self):
        player.rotate()
        player.cast_rays()


class Wall(object):

    def __init__(self, pos):
        self.wall_image = pygame.image.load("floor1.png").convert_alpha()
        self.wall_image.set_alpha(50)
        walls.append(self)
        self.wall_rect = pygame.Rect(pos[0], pos[1], 40, 40)


class Enemy(object):

    def __init__(self, pos):
        enemies.append(self)
        self.enemy_rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.enemy_image = pygame.image.load("Spider.png").convert_alpha()
        self.enemy_rot_image = self.enemy_image
        self.enemy_rot_image_rect = self.enemy_rect

    def move_towards_player(self):
        dx, dy = player.player_rect.x - self.enemy_rect.x, player.player_rect.y - self.enemy_rect.y
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist
        except ZeroDivisionError:
            dx, dy = dx, dy
        self.enemy_rect.x += dx * 3
        self.enemy_rect.y += dy * 3

    def enemy_rotate(self):
        dx, dy = player.player_rect.centerx - self.enemy_rect.centerx, player.player_rect.centery - self.enemy_rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) + 90
        self.enemy_rot_image = pygame.transform.rotate(self.enemy_image, self.angle)
        self.enemy_rot_image_rect = self.enemy_rot_image.get_rect(center=self.enemy_rect.center)

    def enemy_update(self):
        for enemy in enemies:
            enemy.move_towards_player()
            enemy.enemy_rotate()



# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get the treasure!")
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
walls = []
enemies = []
player = Player()

level = (
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W        WW                  W"
    "W        WW                  W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W                            W"
    "W          T                 W"
    "W                            W"
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
)

x = y = 0
for rows in range(30):
    for columns in range(30):
        square = rows*30+columns
        if level[square] == "W":
            Wall((x, y))
        if level[square] == "T":
            end_rect = pygame.Rect(x, y, 20, 20)
        x += 40
    y += 40
    x = 0

enemies_generated = random.randrange(1, 4)
for i in range(enemies_generated):
    enemy_x, enemy_y = random.randrange(100, 1000), random.randrange(100, 1000)
    Enemy((enemy_x, enemy_y))


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
    if key[pygame.K_a]:
        player.move(-4, 0)
    if key[pygame.K_d]:
        player.move(4, 0)
    if key[pygame.K_w]:
        player.move(0, -4)
    if key[pygame.K_s]:
        player.move(0, 4)

    if player.player_rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    screen.fill((255, 255, 255))
    for wall in walls:
        screen.blit(wall.wall_image, wall.wall_rect)
    screen.blit(player.treasure_image, end_rect)
    screen.blit(player.rot_image, player.rot_image_rect)
    player.player_update()
    for enemy in enemies:
        screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)
        enemy.enemy_update()
    pygame.display.flip()  # flip/update?
    clock.tick(360)

pygame.quit()