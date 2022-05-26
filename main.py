import random

import pygame
from sys import exit
import Classes
from pygame import mixer
import json
#//////////////////////////////////////
import main

save_data = {
    'high_score': 0
}
try:
    with open('save_data.txt') as save_file:
        save_data = json.load(save_file)
except:
    print("Save file not found!")
print(save_data['high_score'])


def Reset():
    pipe_group.empty()
    bird.empty()
    bird.add(Classes.Bird())
    main.gameActive = True
    main.gameEnd = False
    main.offset = 0
    main.font_text = "0"

    main.pipe_bool = False
    main.pipe_index = 0

    main.score = 0

def checkCollision():
    if pygame.sprite.spritecollide(bird.sprite, pipe_group, False): return True
    if bird.sprites()[0].rect.bottom > 450: return True


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GAME_NAME = "PyGame"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME_NAME")
clock = pygame.time.Clock()
font = pygame.font.Font("fonts/04B_19__.ttf", 50)

BackGround_Surf = pygame.image.load("graphics/BackGround_1.png").convert()
score_sfx = mixer.Sound("media/Score.mp3")


# Setup
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

pipe_bool = False
pipe_index = 0

score = 0

#/////////////////////////////////////

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            with open('save_data.txt', 'w') as save_file:
                json.dump(save_data, save_file)
            pygame.quit()
            exit()
        if event.type == pipe_timer and gameEnd == False:
            offset = random.randint(0, 150)
            pipe_group.add(Classes.Pipe("Upside", offset))
            pipe_group.add(Classes.Pipe("Downside", offset))
        if event.type == pygame.KEYDOWN and gameEnd:
            if event.key == pygame.K_SPACE:
                Reset()

    font_surface = font.render(font_text, False, 'White')
    font_rect = font_surface.get_rect(center=(CENTER[0], SCREEN_HEIGHT // 9))
    if gameEnd == False: font_text = str(score)
    else: font_text = f'High Score: {save_data["high_score"]}'

    if score > save_data['high_score']: save_data['high_score'] = score

    # SCORE COUNTER  * NO LE MUEVAS :( * //////////////////////////////////////
    if len(bird) > 0 and len(pipe_group) > 0:
        if bird.sprites()[0].rect.left > pipe_group.sprites()[pipe_index].rect.left \
                and bird.sprites()[0].rect.right < pipe_group.sprites()[pipe_index].rect.right and \
                pipe_bool == False:
            pipe_bool = True

        elif pipe_bool and bird.sprites()[0].rect.right > pipe_group.sprites()[pipe_index].rect.right:
            pipe_bool = False
            score_sfx.play()
            score += 1
            if pipe_index == 0: pipe_index = 2
    # //////////////////////////////////////////////////////////////


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
