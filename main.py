import os
import sys
import pygame
import pygame.gfxdraw
import math
import random


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))
        self.treasure_image = pygame.image.load("Assets/Treasure.png").convert_alpha()
        self.background = pygame.image.load("Assets/Background.jpg").convert_alpha()
        self.player_score = 0
        pygame.display.set_caption("Wizarynth")
        icon = pygame.image.load("Assets/Icon.png")
        pygame.display.set_icon(icon)
        self.missile_sound = pygame.mixer.Sound("Music/gra-sopelekspell.mp3")
        self.hit_sound = pygame.mixer.Sound("Music/gra-hitsound.mp3")
        self.death_sound = pygame.mixer.Sound("Music/gra-playerdeath.mp3")
        self.chest_sound = pygame.mixer.Sound("Music/gra-skrzynka.mp3")
        pygame.mixer.music.load("Music/gra-music.mp3")
        self.music_volume = 1
        self.sound_volume = 1
        pygame.mixer.music.play(-1, 0)
        self.clock = pygame.time.Clock()
        self.walls = []
        self.floors = []
        self.enemies = []
        self.level = (
            "WWWWWWWWWWWWWWWWWWWWWWWWW"
            "W           W W         W"
            "W W WWWW  W W W WWW   W W"
            "W W   W   W             W"
            "W W W W W WWWWW WWW   WWW"
            "W W       W     W W W   W"
            "W WWW W WWW WWW   W W WWW"
            "W W   W       W W   W   W"
            "W W W WWW     WWWWWWWWW W"
            "W             W W       W"
            "WWW W WWW W W W W W W WWW"
            "W W   W   W   W   W W   W"
            "W W WWW   W WWW WWWWW W W"
            "W   W     W       W     W"
            "W W W W WWW   WWW WWW W W"
            "W W   W W     W   W W W W"
            "W W   WWWWWW  WWWWW W WWW"
            "W     W W W             W"
            "W WWW W W W W WW  W WWW W"
            "W       W   W W         W"
            "W       W W WWWW  WWW W W"
            "W W W         W     W W W"
            "W W W WWWWW WWW WWWWWWW W"
            "W     W     W           W"
            "WWWWWWWWWWWWWWWWWWWWWWWWW"
        )
        self.offset = pygame.math.Vector2()

    def generate_maze(self):
        x = y = 0
        for rows in range(25):
            for columns in range(25):
                square = rows * 25 + columns
                if self.level[square] == "W":
                    Wall((x, y))
                if self.level[square] == " ":
                    Floor((x, y))
                x += 128
            y += 128
            x = 0

    def generate_enemies(self):
        enemies_generated = 10
        for i in range(enemies_generated):
            enemy_generated_correctly = False
            while not enemy_generated_correctly:
                enemy_x, enemy_y = random.randrange(129, 3073), random.randrange(129, 3073)
                col1 = int(enemy_x/128)
                row1 = int(enemy_y/128)
                col2 = int((enemy_x+95)/128)
                row2 = int((enemy_y+95)/128)
                upper_left = row1*25+col1
                upper_right = row2*25+col1
                down_right = row2*25+col2
                down_left = row1*25+col2
                if self.level[upper_left] == " " and self.level[upper_right] == " " and self.level[down_left] == " " and self.level[down_right] == " ":
                    Enemy((enemy_x, enemy_y))
                    enemy_generated_correctly = True

    def generate_treasure(self):
        treasure_generated_correctly = False
        while not treasure_generated_correctly:
            treasure_x, treasure_y = random.randrange(129, 3073), random.randrange(129, 3073)
            col1 = int(treasure_x / 128)
            row1 = int(treasure_y / 128)
            col2 = int((treasure_x + 64) / 128)
            row2 = int((treasure_y + 64) / 128)
            upper_left = row1 * 25 + col1
            upper_right = row2 * 25 + col1
            down_right = row2 * 25 + col2
            down_left = row1 * 25 + col2
            if self.level[upper_left] == " " and self.level[upper_right] == " " and self.level[down_left] == " " and self.level[down_right] == " ":
                self.treasure_rect = self.treasure_image.get_rect(topleft=(treasure_x+self.offset.x, treasure_y+self.offset.y))
                treasure_generated_correctly = True

    def score(self):
        if player.player_rect.colliderect(self.treasure_rect):
            game.generate_treasure()
            self.player_score +=1
            self.chest_sound.play()

        def get_font(size):
            return pygame.font.Font("Fonts/ka1.ttf", size)

        SCORE_TEXT = get_font(50).render(f"Score: {self.player_score}", True, "#b68f40")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(960, 50))
        self.screen.blit(SCORE_TEXT, SCORE_RECT)

    def play(self):
        self.play_running = True
        while self.play_running:

            game.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.play_running = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and player.missile_time == 0 and player.time_between_shots >= 5:
                    player.generate_missile()
                    player.time_between_shots = 0

            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                player.move(-10, 0)
            if key[pygame.K_d]:
                player.move(10, 0)
            if key[pygame.K_w]:
                player.move(0, -10)
            if key[pygame.K_s]:
                player.move(0, 10)

            self.screen.fill((25, 25, 25))

            for floor in self.floors:
                if player.ground_rect.colliderect(floor.floor_rect):
                    game.screen.blit(floor.floor_image, floor.floor_rect)

            player.player_update()
            game.score()

            self.screen.blit(player.rot_image, player.rot_image_rect)

            for wall in self.walls:
                if player.ground_rect.colliderect(wall.wall_rect):
                    self.screen.blit(wall.wall_image, wall.wall_rect)

            player.time_between_shots += 0.05
            if player.missile_generated:
                player.magic_missile()

            for enemy in self.enemies:
                if player.missile_rect.colliderect(enemy.enemy_rect):
                    enemy.is_frozen = True
                    self.hit_sound.play()
                    player.destroy_missile()
                if enemy.freeze_timer > 3:
                    enemy.freeze_timer = 0
                    enemy.is_frozen = False
                if enemy.is_frozen:
                    enemy.freeze_timer += 0.05
                enemy.enemy_rotate()
                enemy.enemy_cast_rays()
                if enemy.player_visable:
                    enemy.move_towards_player()
                else:
                    enemy.timer += 0.05
                    if enemy.timer < 10:
                        enemy.move_towards_player()
                    else:
                        enemy.move_random_direction()
                if enemy.is_frozen and enemy.enemy_visable:
                    self.screen.blit(enemy.enemy_frozen_rot_image, enemy.enemy_rot_image_rect)
                elif enemy.enemy_visable and not enemy.is_frozen:
                    self.screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

            pygame.display.flip()  # flip/update?
            game.clock.tick(360)

    def get_font(self, size):
        return pygame.font.Font("Fonts/ka1.ttf", size)

    def main_menu(self):
        self.menu_running = True
        while self.menu_running:
            self.screen.blit(self.background, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = game.get_font(120).render("Main menu", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(945, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("Assets/Play Rect.png"), pos=(945, 250),
                                 text_input="Play", font=game.get_font(80), base_color="Grey", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("Assets/Options Rect.png"), pos=(945, 850),
                                 text_input="Options", font=game.get_font(80), base_color="Grey", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("Assets/Quit Rect.png"), pos=(945, 1000),
                                 text_input="Quit", font=game.get_font(80), base_color="Grey", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.screen)

            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                        game.play()
                    if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                        game.options()

            pygame.display.flip()

    def options(self):
        options_running = True
        while options_running:
            self.screen.blit(self.background, (0, 0))

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            VOLUME_TEXT = game.get_font(80).render("Music volume", True, "#b68f40")
            VOLUME_RECT = VOLUME_TEXT.get_rect(center=(945, 200))
            VOLUME_SCAlE = game.get_font(50).render(f"{int(self.music_volume*100)}", True, "#b68f40")
            VOLUME_SCAlE_RECT = VOLUME_SCAlE.get_rect(center=(945, 400))
            SOUND_TEXT = game.get_font(80).render("Sound volume", True, "#b68f40")
            SOUND_RECT = SOUND_TEXT.get_rect(center=(945, 700))
            SOUND_SCAlE = game.get_font(50).render(f"{int(self.sound_volume * 100)}", True, "#b68f40")
            SOUND_SCAlE_RECT = SOUND_SCAlE.get_rect(center=(945, 900))
            self.screen.blit(VOLUME_TEXT, VOLUME_RECT)
            self.screen.blit(VOLUME_SCAlE, VOLUME_SCAlE_RECT)
            self.screen.blit(SOUND_TEXT, SOUND_RECT)
            self.screen.blit(SOUND_SCAlE, SOUND_SCAlE_RECT)

            VOLUME_PLUS = Button(image=pygame.image.load("Assets/Plus.png"), pos=(1190, 400),
                                 text_input="", font=game.get_font(80), base_color="#d7fcd4", hovering_color="White")
            VOLUME_MINUS = Button(image=pygame.image.load("Assets/Minus.png"), pos=(700, 400),
                                 text_input="", font=game.get_font(80), base_color="#d7fcd4", hovering_color="White")
            SOUND_PLUS = Button(image=pygame.image.load("Assets/Plus.png"), pos=(1190, 900),
                                 text_input="", font=game.get_font(80), base_color="#d7fcd4", hovering_color="White")
            SOUND_MINUS = Button(image=pygame.image.load("Assets/Minus.png"), pos=(700, 900),
                                 text_input="", font=game.get_font(80), base_color="#d7fcd4", hovering_color="White")


            for button in [VOLUME_PLUS, VOLUME_MINUS, SOUND_PLUS, SOUND_MINUS]:
                button.change_color(OPTIONS_MOUSE_POS)
                button.update(self.screen)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    options_running = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if VOLUME_PLUS.check_for_input(OPTIONS_MOUSE_POS):
                        if self.music_volume <= 0.9:
                            self.music_volume += 0.1
                            pygame.mixer.music.set_volume(self.music_volume)
                    if VOLUME_MINUS.check_for_input(OPTIONS_MOUSE_POS):
                        if self.music_volume >= 0.1:
                            self.music_volume -= 0.1
                            pygame.mixer.music.set_volume(self.music_volume)
                    if SOUND_PLUS.check_for_input(OPTIONS_MOUSE_POS):
                        if self.sound_volume <= 0.9:
                            self.sound_volume += 0.1
                            self.missile_sound.set_volume(self.sound_volume)
                            self.hit_sound.set_volume(self.sound_volume)
                            self.death_sound.set_volume(self.sound_volume)
                            self.chest_sound.set_volume(self.sound_volume)
                    if SOUND_MINUS.check_for_input(OPTIONS_MOUSE_POS):
                        if self.sound_volume >= 0.1:
                            self.sound_volume -= 0.1
                            self.missile_sound.set_volume(self.sound_volume)
                            self.hit_sound.set_volume(self.sound_volume)
                            self.death_sound.set_volume(self.sound_volume)
                            self.chest_sound.set_volume(self.sound_volume)

            pygame.display.flip()

    def death_screen(self):
        death_running = True
        while death_running:
            self.screen.fill((138, 3, 3))

            DEATH_MOUSE_POS = pygame.mouse.get_pos()

            DEATH_TEXT = game.get_font(100).render("You Died!", True, (0, 0, 0))
            DEATH_RECT = DEATH_TEXT.get_rect(center=(960, 400))
            SCORE_TEXT = game.get_font(50).render(f"Your score: {game.player_score}", True, (0, 0, 0))
            SCORE_RECT = SCORE_TEXT.get_rect(center=(960, 500))
            self.screen.blit(DEATH_TEXT, DEATH_RECT)
            self.screen.blit(SCORE_TEXT, SCORE_RECT)

            BACK_BUTTON = Button(image=pygame.image.load("Assets/Play Rect.png"), pos=(960, 800),
                                 text_input="Back", font=game.get_font(80), base_color="Grey", hovering_color="White")

            for button in [BACK_BUTTON]:
                button.change_color(DEATH_MOUSE_POS)
                button.update(self.screen)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.menu_running = False
                    self.play_running = False
                    death_running = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(DEATH_MOUSE_POS):
                        self.menu_running = False
                        self.play_running = False
                        death_running = False

            pygame.display.flip()


class Player(object):

    def __init__(self):
        self.player_image = pygame.image.load("Assets/wizard.png").convert_alpha()
        self.missile_image = pygame.image.load("Assets/Missile.png").convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(960, 540))
        self.death_rect = pygame.Rect(self.player_rect.centerx - 5, self.player_rect.centery - 5, 10, 10)
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
        game.offset.x -= dx
        game.offset.y -= dy
        game.treasure_rect.centerx -= dx
        game.treasure_rect.centery -= dy
        for floor in game.floors:
            floor.floor_rect.x -= dx
            floor.floor_rect.y -= dy
        for enemy in game.enemies:
            enemy.enemy_rect.x -= dx
            enemy.enemy_rect.y -= dy
        for wall in game.walls:
            wall.wall_rect.x -= dx
            wall.wall_rect.y -= dy
            if self.player_rect.colliderect(wall.wall_rect):
                game.offset.x += dx
                game.offset.y += dy
                self.missile_rect.centerx += dx
                self.missile_rect.centery += dy
                game.treasure_rect.centerx += dx
                game.treasure_rect.centery += dy
                for floor in game.floors:
                    floor.floor_rect.x += dx
                    floor.floor_rect.y += dy
                for enemy in game.enemies:
                    enemy.enemy_rect.x += dx
                    enemy.enemy_rect.y += dy
                for wall in game.walls:
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
        game.missile_sound.play()

    def magic_missile(self):
        global missile_direction
        game.screen.blit(self.missile_image, self.missile_rect)
        if self.missile_time == 0:
            mx, my = pygame.mouse.get_pos()
            missile_direction = pygame.math.Vector2(mx - player.player_rect.centerx, my - player.player_rect.centery)
            missile_direction.normalize()
        missile_direction.scale_to_length(50)
        self.missile_rect.move_ip(missile_direction)
        self.missile_time += 0.05
        for wall in game.walls:
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
        for enemy in game.enemies:
            enemy.enemy_lock = False
        for ray in range(31):
            for depth in range(25):
                target_x = self.player_rect.centerx - math.sin(start_angle) * depth * 30
                target_y = self.player_rect.centery - math.cos(start_angle) * depth * 30
                raycast_rect = pygame.Rect(target_x, target_y, 1, 1)
                if raycast_rect.colliderect(game.treasure_rect):
                    game.screen.blit(game.treasure_image, game.treasure_rect)
                for enemy in game.enemies:
                    if raycast_rect.colliderect(enemy.enemy_rect):
                        enemy.enemy_visable = True
                        enemy.enemy_lock = True
                    if not raycast_rect.colliderect(enemy.enemy_rect) and not enemy.enemy_lock:
                        enemy.enemy_visable = False
                for wall in game.walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        # pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                        points.append((target_x, target_y))
                        game.screen.blit(wall.wall_image, wall.wall_rect)
                        break
                    # else:
                    # pygame.draw.line(screen, (255, 255, 0), (self.player_rect.centerx, self.player_rect.centery), (target_x, target_y), 4)
                else:
                    continue
                break
            points.append((target_x, target_y))
            start_angle += math.pi / 90

        for point in points:
            pygame.gfxdraw.filled_polygon(game.screen, (point, starting_point, self.player_rect.center),
                                          (255, 255, 100, 4))
            starting_point = point
            # pygame.draw.circle(screen, (0, 255, 255), point, 5)
            # screen.blit(enemy.enemy_rot_image, enemy.enemy_rot_image_rect)

    def player_update(self):
        player.rotate()
        player.cast_rays()
        player.player_death()

    def player_death(self):
        for enemy in game.enemies:
            if enemy.enemy_rect.colliderect(self.death_rect) and not enemy.is_frozen:
                game.death_sound.play()
                game.death_screen()


class Wall(object):

    def __init__(self, pos):
        self.wall_image = pygame.image.load("Assets/Wall.png").convert_alpha()
        self.wall_image.set_alpha(50)
        game.walls.append(self)
        self.wall_rect = pygame.Rect(pos[0], pos[1], 128, 128)


class Floor(object):

    def __init__(self, pos):
        self.floor_image = pygame.image.load("Assets/Floor.png").convert_alpha()
        self.floor_image.set_alpha(50)
        game.floors.append(self)
        self.floor_rect = pygame.Rect(pos[0], pos[1], 128, 128)


class Enemy(object):

    def __init__(self, pos):
        game.enemies.append(self)
        self.enemy_rect = pygame.Rect(pos[0], pos[1], 95, 95)
        self.enemy_image = pygame.image.load("Assets/Monster.png").convert_alpha()
        self.enemy_frozen_image = pygame.image.load("Assets/Frozen_Monster.png").convert_alpha()
        self.enemy_rot_image = self.enemy_image
        self.enemy_rot_image_rect = self.enemy_rect
        self.enemy_frozen_rot_image = self.enemy_frozen_image
        self.player_visable = False
        self.enemy_visable = False
        self.reset_function = True
        self.enemy_lock = False
        self.point_of_interest = (random.randrange(0, 1920), random.randrange(0, 1080))
        self.temporary_point = self.point_of_interest
        self.direction = random.randrange(0, 4)
        self.timer = 10
        self.freeze_timer = 0
        self.is_frozen = False

    def move_towards_player(self):
        if self.player_visable:
            self.timer = 0
        dirvect = pygame.math.Vector2(player.player_rect.x - self.enemy_rect.x, player.player_rect.y - self.enemy_rect.y)
        try:
            dirvect.normalize()
        except ValueError:
            dirvect.x += 0.01
            dirvect.y += 0.01
        dirvect.scale_to_length(15)
        if not self.is_frozen:
            self.enemy_rect.move_ip(dirvect)
        for wall in game.walls:
            if self.enemy_rect.colliderect(wall.wall_rect):
                self.enemy_rect.move_ip(-dirvect)
                if wall.wall_rect.bottom == self.enemy_rect.top:
                    if dirvect.x > 0 and dirvect.y < 0:
                        self.enemy_rect.x += 12
                    if dirvect.x < 0 and dirvect.y < 0:
                        self.enemy_rect.x -= 12
                elif wall.wall_rect.top == self.enemy_rect.bottom:
                    if dirvect.x > 0 and dirvect.y > 0:
                        self.enemy_rect.x += 12
                    if dirvect.x < 0 and dirvect.y > 0:
                        self.enemy_rect.x -= 12
                elif wall.wall_rect.left == self.enemy_rect.right:
                    if dirvect.x > 0 and dirvect.y < 0:
                        self.enemy_rect.y -= 12
                    if dirvect.x > 0 and dirvect.y > 0:
                        self.enemy_rect.y += 12
                elif wall.wall_rect.right == self.enemy_rect.left:
                    if dirvect.x < 0 and dirvect.y < 0:
                        self.enemy_rect.y -= 12
                    if dirvect.x < 0 and dirvect.y > 0:
                        self.enemy_rect.y += 12

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
        for wall in game.walls:
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
        if self.player_visable or self.timer < 10:
            dx, dy = player.player_rect.centerx - self.enemy_rect.centerx, player.player_rect.centery - self.enemy_rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) + 90
        self.enemy_rot_image = pygame.transform.rotate(self.enemy_image, self.angle)
        self.enemy_frozen_rot_image = pygame.transform.rotate(self.enemy_frozen_image, self.angle)
        self.enemy_rot_image_rect = self.enemy_rot_image.get_rect(center=self.enemy_rect.center)

    def enemy_cast_rays(self):
        start_angle = math.radians(self.angle) - math.pi / 2
        lock = False
        for ray in range(21):
            for depth in range(10):
                enemy_target_x = self.enemy_rect.centerx + math.sin(start_angle) * depth * 75
                enemy_target_y = self.enemy_rect.centery + math.cos(start_angle) * depth * 75
                raycast_rect = pygame.Rect(enemy_target_x, enemy_target_y, 1, 1)
                if raycast_rect.colliderect(player.player_rect):
                    self.player_visable = True
                    lock = True
                elif not lock:
                    self.player_visable = False
                for wall in game.walls:
                    if raycast_rect.colliderect(wall.wall_rect):
                        #pygame.draw.line(game.screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (enemy_target_x, enemy_target_y), 4)
                        break
                    #else:
                        #pygame.draw.line(game.screen, (255, 255, 0), (self.enemy_rect.centerx, self.enemy_rect.centery), (enemy_target_x, enemy_target_y), 4)
                else:
                    continue
                break
            start_angle += math.pi / 20


class Button(object):
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
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


os.environ["SDL_VIDEO_CENTERED"] = "1"


pygame.init()

running = True
while running:
    game = Game()
    player = Player()
    game.generate_maze()
    game.generate_enemies()
    game.generate_treasure()
    game.main_menu()

pygame.quit()
