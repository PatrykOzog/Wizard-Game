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
        self.missile_image = pygame.image.load("Missile.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(960, 540))
        self.missile_rect = self.missile_image.get_rect(center=(0, 0))
        self.rot_image = self.player_image
        self.rot_image_rect = self.player_rect
        self.ground_rect = pygame.Rect(0, 0, 1920, 1080)
        self.missile_time = 0
        self.time_between_shots = 5
        self.missile_generated = False

    def move(self, dx, dy):
        self.missile_rect.centerx -= dx
        self.missile_rect.centery -= dy
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
                self.missile_rect.centerx += dx
                self.missile_rect.centery += dy
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

    def generate_missile(self):
        self.missile_generated = True
        self.missile_rect.center = self.player_rect.center
        self.missile_time = 0

    def magic_missile(self):
        global missile_direction
        screen.blit(self.missile_image, self.missile_rect)
        if self.missile_time == 0:
            mx, my = pygame.mouse.get_pos()
            missile_direction = pygame.math.Vector2(mx - player.player_rect.centerx, my - player.player_rect.centery)
            missile_direction.normalize()
        missile_direction.scale_to_length(50)
        self.missile_rect.move_ip(missile_direction)
        self.missile_time += 0.05
        for wall in walls:
            if self.missile_rect.colliderect(wall.wall_rect):
                player.destroy_missile()
        if self.missile_time > 1:
            player.destroy_missile()

    def destroy_missile(self):
        self.missile_generated = False
        self.missile_time = 0
        self.missile_rect.center = (10000, 10000)

    def cast_rays(self):
        points = []
        starting_point = (self.player_rect.centerx, self.player_rect.centery)
        start_angle = math.radians(self.angle) - math.pi / 6
        for ray in range(31):
            for depth in range(25):
                target_x = self.player_rect.centerx - math.sin(start_angle) * depth * 30
                target_y = self.player_rect.centery - math.cos(start_angle) * depth * 30
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                # for enemy in enemies:
                #    if raycast_rect.colliderect(enemy.enemy_rect):
                #        screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)
                for wall in walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        # pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                        points.append((target_x, target_y))
                        screen.blit(wall.wall_image, wall.wall_rect)
                        break
                    # else:
                    # pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break
            points.append((target_x, target_y))
            start_angle += math.pi / 90

        for point in points:
            pygame.gfxdraw.filled_polygon(screen, (point, starting_point, self.player_rect.center), (255, 255, 100, 4))
            starting_point = point
            # pygame.draw.circle(screen, (0, 255, 255), point, 5)
            # screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

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
        self.enemy_frozen_image = pygame.image.load("Frozen_Monster.png").convert_alpha()
        self.enemy_rot_image = self.enemy_image
        self.enemy_rot_image_rect = self.enemy_rect
        self.enemy_frozen_rot_image = self.enemy_frozen_image
        self.player_visable = False
        self.reset_function = True
        self.point_of_interest = (random.randrange(0, 1920), random.randrange(0, 1080))
        self.temporary_point = self.point_of_interest
        self.direction = random.randrange(0, 4)
        self.timer = 5
        self.freeze_timer = 0
        self.is_frozen = False

    def move_towards_player(self):
        if self.player_visable:
            self.timer = 0
        dirvect = pygame.math.Vector2(player.player_rect.x - self.enemy_rect.x,
                                      player.player_rect.y - self.enemy_rect.y)
        try:
            dirvect.normalize()
        except ValueError:
            dirvect.x += 0.01
            dirvect.y += 0.01
        dirvect.scale_to_length(10)
        if not self.is_frozen:
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
        if not self.is_frozen:
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
        self.enemy_frozen_rot_image = pygame.transform.rotate(self.enemy_frozen_image, self.angle)
        self.enemy_rot_image_rect = self.enemy_rot_image.get_rect(center=self.enemy_rect.center)

    def enemy_cast_rays(self):
        start_angle = math.radians(self.angle) - math.pi / 2
        lock = False
        for ray in range(31):
            for depth in range(12):
                enemy_target_x = self.enemy_rect.centerx + math.sin(start_angle) * depth * 70
                enemy_target_y = self.enemy_rect.centery + math.cos(start_angle) * depth * 70
                raycast_rect = pygame.Rect(enemy_target_x, enemy_target_y, 1, 1)
                if raycast_rect.colliderect(player.player_rect):
                    self.player_visable = True
                    lock = True
                elif not lock:
                    self.player_visable = False
                for wall in walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        # pygame.draw.line(screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (target_x, target_y), 4)
                        break
                    # else:
                    #    pygame.draw.line(screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break
            start_angle += math.pi / 30

    def frozen(self):
        if player.missile_rect.colliderect(enemy.enemy_rect):
            self.is_frozen = True
            player.destroy_missile()
        if self.freeze_timer > 3:
            self.freeze_timer = 0
            self.is_frozen = False
        if self.is_frozen:
            self.freeze_timer += 0.05

    def enemy_update(self):
        enemy.frozen()
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


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Get the treasure!")
screen = pygame.display.set_mode((1920, 1080))

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
walls = []
floors = []
enemies = []
player = Player()
key_pressed = False

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
        square = rows * 25 + columns
        if level[square] == "W":
            Wall((x, y))
        if level[square] == " ":
            Floor((x, y))
        if level[square] == "T":
            end_rect = pygame.Rect(x, y, 20, 20)
        x += 128
    y += 128
    x = 0

enemies_generated = 2  # random.randrange(1, 4)
for i in range(enemies_generated):
    enemy_x, enemy_y = random.randrange(100, 1000), random.randrange(100, 1000)
    Enemy((enemy_x, enemy_y))

def main_menu():
    BG = pygame.image.load("Background.png")

    def get_font(size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("font.ttf", size)

    menu_running = True
    while menu_running:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    menu_running = False

        pygame.display.flip()

main_menu()
running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and player.missile_time == 0 and player.time_between_shots >= 5:
            player.generate_missile()
            player.time_between_shots = 0

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
        if player.ground_rect.colliderect(floor.floor_rect):
            screen.blit(floor.floor_image, floor.floor_rect)

    screen.blit(player.treasure_image, end_rect)
    player.player_update()
    screen.blit(player.rot_image, player.rot_image_rect)

    for wall in walls:
        if player.ground_rect.colliderect(wall.wall_rect):
            screen.blit(wall.wall_image, wall.wall_rect)

    player.time_between_shots += 0.05
    if player.missile_generated:
        player.magic_missile()

    for enemy in enemies:
        enemy.enemy_update()
        if enemy.is_frozen:
            screen.blit(enemy.enemy_frozen_rot_image, enemy.enemy_rot_image_rect)
        else:
            screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

    # screen.blit(player.missile_image, player.missile_rect)

    pygame.display.flip()  # flip/update?
    clock.tick(360)

pygame.quit()
