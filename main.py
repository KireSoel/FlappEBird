import random

import pygame
from sys import exit
import Classes
#//////////////////////////////////////


def checkCollision():
    if pygame.sprite.spritecollide(bird.sprite, pipe_group, False): return True


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GAME_NAME = "PyGame"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME_NAME")
clock = pygame.time.Clock()
font = pygame.font.Font("fonts/Pixeltype.ttf", 50)

BackGround_Surf = pygame.image.load("graphics/BackGround_1.png").convert()


# ////////////////////////////////////////
bird = pygame.sprite.GroupSingle()
bird.add(Classes.Bird())

pipe_group = pygame.sprite.Group()

pipe_timer = pygame.USEREVENT + 1
timer_seconds = 1000
pygame.time.set_timer(pipe_timer, timer_seconds)
# ////////////////////////////////////////

gameActive = True
gameEnd = False
offset = 0
font_text = "0"

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pipe_timer and gameEnd == False:
            offset = random.randint(0, 150)
            pipe_group.add(Classes.Pipe("Upside", offset))
            pipe_group.add(Classes.Pipe("Downside", offset))

    font_surface = font.render(font_text, False, 'Black')
    font_rect = font_surface.get_rect(center=(CENTER[0], SCREEN_HEIGHT // 9))

    if len(bird) > 0 and len(pipe_group) > 0    :
        if bird.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left:
            font_text = ":)"

    screen.blit(BackGround_Surf, (0, 0))

    gameActive = checkCollision()
    if gameActive: gameEnd = True

    #///////////////////////////////////
    pipe_group.draw(screen)
    pipe_group.update(gameActive)

    bird.draw(screen)
    bird.update(events, gameActive)

    screen.blit(font_surface, font_rect)
    #///////////////////////////////////

    pygame.display.update()
    clock.tick(60)
