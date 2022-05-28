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
gameModeData = {
    'Easy_Gap': 150
}

gameMode = "Easy"

try:
    with open('save_data.txt') as save_file:
        save_data = json.load(save_file)
except:
    print("Save file not found!")

scene = 0

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
    if pygame.sprite.spritecollide(bird.sprite, pipe_group, False):
        return True
    if bird.sprites()[0].rect.bottom > 450:
        return True


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GAME_NAME = "PyGame"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
font = pygame.font.Font("fonts/04B_19__.ttf", 50)

BackGround_Surf = pygame.image.load("graphics/BackGround_1.png").convert()
score_sfx = mixer.Sound("media/Score.mp3")


def ChangeScene(sceneN):
    main.setupBool = False
    main.scene = sceneN

#Splash screen setup



# Setup
# ////////////////////////////////////////
bird = pygame.sprite.GroupSingle()

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

setupBool = False

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            with open('save_data.txt', 'w') as save_file:
                json.dump(save_data, save_file)
            pygame.quit()
            exit()

    if scene == 0:
        if setupBool == False:
            setupBool = True
            splash_font = pygame.font.Font("fonts/Retro Gaming.ttf", 30)
            splash_color = "Black"
            splash_ind = 0
            timer_splash = pygame.time.get_ticks()

        font_surface = splash_font.render("-Splash-", False, splash_color)
        font_rect = font_surface.get_rect(center=(CENTER[0], CENTER[1]))
        font_surface2 = splash_font.render("Screen", False, splash_color)
        font_rect2 = font_surface2.get_rect(center=(CENTER[0], CENTER[1]+25))
        print(f'{pygame.time.get_ticks()} - {timer_splash + 1000}' )

        if pygame.time.get_ticks() > timer_splash + 1000:
            if splash_ind == 0:
                score_sfx.play()
                splash_color = "white"
                timer_splash = pygame.time.get_ticks()
                splash_ind += 1
            else:
                ChangeScene(2)


        screen.fill("Black")
        screen.blit(font_surface, font_rect)
        screen.blit(font_surface2, font_rect2)

    if scene == 2:
        if setupBool == False:
            Reset()
            setupBool = True
        for e in events:
            if e.type == pipe_timer and gameEnd == False:
                offset = random.randint(0, 150)
                pipe_group.add(Classes.Pipe("Upside", offset))
                pipe_group.add(Classes.Pipe("Downside", offset, gameModeData[gameMode+"_Gap"]))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and gameEnd:
                    Reset()
                if e.key == pygame.K_ESCAPE:
                    ChangeScene(0)

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

