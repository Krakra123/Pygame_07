import sys
import os
import math
import random
import pygame

import Components
from GameVariable import GameVariable

pygame.init()

DISPLAY = pygame.display.set_mode((GameVariable.WITDH, GameVariable.HEIGHT))
pygame.display.set_caption(f"DINO - Lil Tuan Nghia")

gameVariable = GameVariable()
clock = pygame.time.Clock()

# Game
game_speed = gameVariable.game_speed
game_over = False

on_ground = True

jump_force = 14

key_pressing = False
instance_press = False
press_time = 0

track_time = 0

cactus_time = 0

walk_status = 0
walk_time = 0

score = 0
high_score = 0

font = pygame.font.Font(f"./Assets/PressStart2P-Regular.ttf", 16)
end_font = pygame.font.Font(f"./Assets/PressStart2P-Regular.ttf", 32)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.transform = Components.Transform(self, (120, gameVariable.ground_level), 0, (1, 1))
        self.rigidbody = Components.Rigidbody(self, self.transform)

    def Sprite(self, asset_dir):
        self.image = pygame.image.load(asset_dir)
        self.rect = self.image.get_rect()

    def update(self):
        self.transform.update()
        self.rigidbody.update()

    def get(self):
        return "Dino"

class Track(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.transform = Components.Transform(self, (gameVariable.WITDH, gameVariable.ground_level + 6), 0, (1, 1))
        self.rigidbody = Components.Rigidbody(self, self.transform)
        self.rigidbody.gravity = 0;

    def Sprite(self, asset_dir):
        self.image = pygame.image.load(asset_dir)
        self.rect = self.image.get_rect()

    def update(self):
        self.rigidbody.set_velocity((-gameVariable.game_speed, 0))
        self.rigidbody.update()

    def get(self):
        return "Track"

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.transform = Components.Transform(self, (gameVariable.WITDH, gameVariable.ground_level), 0, (1, 1))
        self.rigidbody = Components.Rigidbody(self, self.transform)
        self.rigidbody.gravity = 0;

    def Sprite(self, asset_dir):
        self.image = pygame.image.load(asset_dir)
        self.rect = self.image.get_rect()

    def update(self):
        self.rigidbody.set_velocity((-gameVariable.game_speed, 0))
        self.rigidbody.update()

    def get(self):
        return "Cactus"

class UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.transform = Components.Transform(self, (gameVariable.WITDH, gameVariable.ground_level), 0, (1, 1))

    def Sprite(self, asset_dir):
        self.image = pygame.image.load(asset_dir)
        self.rect = self.image.get_rect()

    def update(self):
        self.transform.update()

    def get(self):
        return "UI"

draw_data = pygame.sprite.Group()

player = Player()

def draw_text(text, font, color, pos):
    display_text = font.render(text, True, color, pygame.color.Color("white"))
    text_rect = display_text.get_rect()
    text_rect.center = pos
    DISPLAY.blit(display_text, text_rect)

def first_track():
    first_track = Track()
    first_track.Sprite(f"./Assets/Other/Track.png")
    first_track.transform.set_position((gameVariable.WITDH - 2350, gameVariable.ground_level + 6))
    draw_data.add(first_track)

def reset():
    for obj in draw_data: draw_data.remove(obj)
    global game_speed
    global track_time
    global cactus_time
    global walk_status
    global walk_time
    global score

    game_speed = GameVariable.game_speed
    track_time = 0
    cactus_time = 0
    walk_status = 0
    walk_time = 0
    score = 0

    gameVariable.ingame_time = 0
    first_track()

# Init
player.Sprite(f"./Assets/Dino/Dino_2.png")

# Game
first_track()
while True:

    # FPS count
    clock.tick()

    # Game Variable
    gameVariable.current_fps = clock.get_fps()
    if (gameVariable.current_fps < 5): continue
    gameVariable.ingame_time += (1 / gameVariable.current_fps)
    game_speed += (1 / gameVariable.current_fps) / 4
    game_speed = min(game_speed, 60)

    # Game Over
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                reset()
                game_over = False
        continue

    # Event
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            sys.exit()

        # Input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                key_pressing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                key_pressing = False

    if key_pressing:
        press_time += (1 / gameVariable.current_fps)
    else:
        if press_time != 0 and press_time <= 0.1: 
            instance_press = True
        press_time = 0

    # Game

    # Track
    def track_delay():
        v = gameVariable.game_speed * gameVariable.PIXEL_PER_DISTANCE
        a = max((1 / gameVariable.current_fps) / 4, 0.0001)
        return (-v + math.sqrt(v * v + 2 * 2350 * a)) / a
    if (gameVariable.ingame_time >= track_time):
        track = Track()
        track.Sprite(f"./Assets/Other/Track.png")
        draw_data.add(track)

        track_time += track_delay()

    # Cactus
    def cactus_delay():
        return 0.8 + (random.randrange(0, 60) / 100)
    if (gameVariable.ingame_time >= cactus_time):
        cactus = Cactus()
        cactus.Sprite(f"./Assets/Cactus/Cactus_{random.randrange(0, 7)}.png")
        draw_data.add(cactus)

        cactus_time += cactus_delay()

    # Player

    # Ground check
    if player.transform.position[1] >= gameVariable.ground_level:
        on_ground = True
        player.transform.set_position((player.transform.position[0], gameVariable.ground_level))
        player.rigidbody.set_velocity((player.rigidbody.velocity[0], 0))
    else:                                 
        on_ground = False

    # Jump
    if on_ground and key_pressing:
        player.rigidbody.set_velocity((player.rigidbody.velocity[0], -jump_force))

    # Gravity (better)
    gravity_multiply = 1
    if not on_ground:
        if instance_press: 
            gravity_multiply = 1.77
    else:
        instance_press = False
    if on_ground:
        player.rigidbody.gravity = gameVariable.GRAVITY
    else:
        if player.rigidbody.velocity[1] <= 0:
            player.rigidbody.gravity = gameVariable.GRAVITY * 4 * gravity_multiply

    player.rigidbody.gravity_update()

    # Animation
    def walk_delay():
        return 0.15 * (100 - gameVariable.game_speed) / 100
    if on_ground:
        if walk_time >= walk_delay():
            walk_status = 1 - walk_status
            player.Sprite(f"./Assets/Dino/Dino_{walk_status}.png")
            walk_time = 0
        else:
            walk_time += (1 / gameVariable.current_fps)
    else:
        player.Sprite(f"./Assets/Dino/Dino_2.png")

    DISPLAY.fill(pygame.color.Color(("white")))

    # Collision
    for sprite in draw_data:
        if sprite.get() == "Cactus":
            if player.transform.position[0] + player.rect.size[0] - 30 >= sprite.transform.position[0] + 10 and player.transform.position[0] + 30 <= sprite.transform.position[0] + sprite.rect.size[0] - 10 and player.transform.position[1] - 10 >= sprite.transform.position[1] - sprite.rect.size[1] + 10:
                # Game Over
                player.Sprite(f"./Assets/Dino/Dino_5.png")
                over = UI()
                over.Sprite(f"./Assets/Other/GameOver.png")
                over.transform.set_position((GameVariable.WITDH / 2 - over.rect.size[0] / 2, GameVariable.HEIGHT / 2 + over.rect.size[1] / 2 - 180))
                restart = UI()
                restart.Sprite(f"./Assets/Other/Reset.png")
                restart.transform.set_position((GameVariable.WITDH / 2 - restart.rect.size[0] / 2, GameVariable.HEIGHT / 2 + restart.rect.size[1] / 2 - 120))

                draw_data.add(over)
                draw_data.add(restart)

                draw_text("- "+str(int(score))+" -", end_font, (83, 83, 83), (gameVariable.WITDH / 2, GameVariable.HEIGHT / 2 - 45))

                high_score = max(high_score, score)

                game_over = True

    # Draw

    # UI
    score += (1 / gameVariable.current_fps) * 69
    score_text = str(int(score)).zfill(8)
    draw_text(score_text, font, (83, 83, 83), (gameVariable.WITDH - 80, 20))

    high_score_text = str(int(high_score)).zfill(8)
    draw_text(high_score_text, font, pygame.color.Color("Gray"), (gameVariable.WITDH - 230, 20))

    # Main 
    for sprite in draw_data:
        if sprite.rect.bottomleft[0] + sprite.rect.size[0] < -10:
            draw_data.remove(sprite)

    draw_data.remove(player)
    draw_data.add(player)

    draw_data.update()
    draw_data.draw(DISPLAY)

    pygame.display.update()