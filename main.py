import os
import sys
import pygame
import pygame.gfxdraw
import math
import random


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("wizard.png").convert_alpha()
        self.treasure_image = pygame.image.load("Treasure.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(960, 540))
        self.rot_image = self.player_image
        self.rot_image_rect = self.player_rect

    def move(self, dx, dy):
        for floor in floors:
            floor.floor_rect.x -= dx
            floor.floor_rect.y -= dy
        for enemy in enemies:
            enemy.enemy_rect.x -= dx
            enemy.enemy_rect.y -= dy
        for wall in walls:
            wall.wall_rect.x -= dx
            wall.wall_rect.y -= dy
            if self.player_rect.colliderect(wall.wall_rect):
                for floor in floors:
                    floor.floor_rect.x += dx
                    floor.floor_rect.y += dy
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
            for depth in range(25):
                target_x = self.player_rect.centerx - math.sin(start_angle) * depth * 30
                target_y = self.player_rect.centery - math.cos(start_angle) * depth * 30
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                for enemy in enemies:
                    if raycast_rect.colliderect(enemy.enemy_rect):
                        screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)
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
            pygame.gfxdraw.filled_polygon(screen, (point, starting_point, self.player_rect.center), (255, 255, 100, 4))
            starting_point = point
            #pygame.draw.circle(screen, (0, 255, 255), point, 5)
            #screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

    def player_update(self):
        player.rotate()
        player.cast_rays()


class Wall(object):

    def __init__(self, pos):
        self.wall_image = pygame.image.load("Wall.png").convert_alpha()
        self.wall_image.set_alpha(50)
        walls.append(self)
        self.wall_rect = pygame.Rect(pos[0], pos[1], 128, 128)

class Floor(object):

    def __init__(self, pos):
        self.floor_image = pygame.image.load("Floor.png").convert_alpha()
        self.floor_image.set_alpha(50)
        floors.append(self)
        self.floor_rect = pygame.Rect(pos[0], pos[1], 128, 128)


class Enemy(object):

    def __init__(self, pos):
        enemies.append(self)
        self.enemy_rect = pygame.Rect(pos[0], pos[1], 95, 95)
        self.enemy_image = pygame.image.load("Monster.png").convert_alpha()
        self.enemy_rot_image = self.enemy_image
        self.enemy_rot_image_rect = self.enemy_rect
        self.player_visable = False
        self.reset_function = True
        self.point_of_interest = (random.randrange(0, 1920), random.randrange(0, 1080))
        self.temporary_point = self.point_of_interest
        self.direction = random.randrange(0, 4)
        self.timer = 5

    def move_towards_player(self):
        if self.player_visable:
            self.timer = 0
        dirvect = pygame.math.Vector2(player.player_rect.x - self.enemy_rect.x,  player.player_rect.y - self.enemy_rect.y)
        try:
            dirvect.normalize()
        except ValueError:
            dirvect.x += 0.01
            dirvect.y += 0.01
        dirvect.scale_to_length(10)
        self.enemy_rect.move_ip(dirvect)
        for wall in walls:
            if self.enemy_rect.colliderect(wall.wall_rect):
                self.enemy_rect.move_ip(-dirvect)
                if wall.wall_rect.bottom == self.enemy_rect.top or wall.wall_rect.top == self.enemy_rect.bottom:
                    self.enemy_rect.x += dirvect.x
                if wall.wall_rect.left == self.enemy_rect.right or wall.wall_rect.right == self.enemy_rect.left:
                    self.enemy_rect.y += dirvect.y

    def move_random_direction(self):
        if self.reset_function:
            self.direction = random.randrange(0, 4)
        self.reset_function = False
        if self.direction == 0:
            self.enemy_rect.x += 15
        elif self.direction == 1:
            self.enemy_rect.x -= 15
        elif self.direction == 2:
            self.enemy_rect.y += 15
        elif self.direction == 3:
            self.enemy_rect.y -= 15
        for wall in walls:
            if self.enemy_rect.colliderect(wall.wall_rect):
                if self.direction == 0:
                    self.enemy_rect.x -= 15
                elif self.direction == 1:
                    self.enemy_rect.x += 15
                elif self.direction == 2:
                    self.enemy_rect.y -= 15
                elif self.direction == 3:
                    self.enemy_rect.y += 15
                self.reset_function = True

    def enemy_rotate(self):
        if self.direction == 0:
            dx, dy = 10000, self.enemy_rect.centery
        elif self.direction == 1:
            dx, dy = -10000, -self.enemy_rect.centery
        elif self.direction == 2:
            dx, dy = self.enemy_rect.centerx, 10000
        elif self.direction == 3:
            dx, dy = -self.enemy_rect.centerx, -10000
        if self.player_visable or self.timer < 5:
            dx, dy = player.player_rect.centerx - self.enemy_rect.centerx, player.player_rect.centery - self.enemy_rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) + 90
        self.enemy_rot_image = pygame.transform.rotate(self.enemy_image, self.angle)
        self.enemy_rot_image_rect = self.enemy_rot_image.get_rect(center=self.enemy_rect.center)

    def enemy_cast_rays(self):
        start_angle = math.radians(self.angle) - math.pi / 6
        lock = False
        for ray in range(20):
            for depth in range(12):
                target_x = self.enemy_rect.centerx + math.sin(start_angle) * depth * 70
                target_y = self.enemy_rect.centery + math.cos(start_angle) * depth * 70
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                if raycast_rect.colliderect(player.player_rect):
                    self.player_visable = True
                    lock = True
                elif not lock:
                    self.player_visable = False
                for wall in walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        #pygame.draw.line(screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (target_x, target_y), 4)
                        break
                    #else:
                        #pygame.draw.line(screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break
            start_angle += math.pi / 60

    def enemy_update(self):
        enemy.enemy_rotate()
        enemy.enemy_cast_rays()
        if self.player_visable:
            enemy.move_towards_player()
        else:
            self.timer += 0.05
            if self.timer < 5:
                enemy.move_towards_player()
            else:
                enemy.move_random_direction()

# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get the treasure!")
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
walls = []
floors = []
enemies = []
player = Player()

level = (
    "WWWWWWWWWWWWWWWWWWWWWWWWW"
    "W                       W"
    "W                       W"
    "W        WW             W"
    "W        WW             W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W                       W"
    "W          T            W"
    "W                       W"
    "WWWWWWWWWWWWWWWWWWWWWWWWW"
)

x = y = 0
for rows in range(25):
    for columns in range(25):
        square = rows*25+columns
        if level[square] == "W":
            Wall((x, y))
        if level[square] == " ":
            Floor((x, y))
        if level[square] == "T":
            end_rect = pygame.Rect(x, y, 20, 20)
        x += 128
    y += 128
    x = 0

enemies_generated = 2 #random.randrange(1, 4)
for i in range(enemies_generated):
    enemy_x, enemy_y = random.randrange(100, 1000), random.randrange(100, 1000)
    Enemy((enemy_x, enemy_y))


icon = pygame.image.load("icon.png")
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
        player.move(-18, 0)
    if key[pygame.K_d]:
        player.move(18, 0)
    if key[pygame.K_w]:
        player.move(0, -18)
    if key[pygame.K_s]:
        player.move(0, 18)

    if player.player_rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    screen.fill((25, 25, 25))
    for floor in floors:
        screen.blit(floor.floor_image, floor.floor_rect)
    screen.blit(player.treasure_image, end_rect)
    player.player_update()
    screen.blit(player.rot_image, player.rot_image_rect)
    #screen.blit(player.floor_image, (100, 100))
    for wall in walls:
        screen.blit(wall.wall_image, wall.wall_rect)
    for enemy in enemies:
        enemy.enemy_update()
        #screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)
    pygame.display.flip()  # flip/update?
    clock.tick(360)

pygame.quit()