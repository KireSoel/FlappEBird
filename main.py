import random

import pygame
from sys import exit
import Classes
from pygame import mixer
import json
# //////////////////////////////////////
import main

# "Easy", "Medium", "Hard"
save_data = {
    'game_mode': "Easy",
    'high_score': 0,
    'Easy_high_score': 0,
    'Medium_high_score': 0,
    'Hard_high_score': 0
}
gameModeData = {
    'Easy_Gap': 170,
    'Medium_Gap': 150,
    'Hard_Gap': 125
}

print(save_data['game_mode'])

try:
    with open('save_data.txt') as save_file:
        save_data = json.load(save_file)
except:
    print("Save file not found!")

scene = 0


def Reset(state=1):
    mixer.stop()
    mixer.music.load("media/NormalTheme.mp3")
    mixer.music.set_volume(0.75)
    # mixer.music.play(-1)

    pipe_group.empty()
    bird.empty()
    bird.add(Classes.Bird())
    main.gameActive = True
    if state == 0:
        main.gameStart = True
    else:
        main.gameStart = False
    main.gameEnd = False
    main.offset = 0
    main.font_text = "0"

    main.GameOverActivateBool = False
    main.FinalGameOverBool = False
    main.gameOver_Played = False

    main.pipe_bool = False
    main.pipe_index = 0

    main.MenuBtn.Visible = False
    main.RestBtn.Visible = False
    main.GOScreen_Vis = False

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
gameOver_sfx = mixer.Sound("media/GameOver.mp3")
gameOver_Played = False


def ChangeScene(sceneN):
    mixer.music.stop()
    main.setupBool = False
    main.scene = sceneN


# Splash screen setup


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
gameStart = False
offset = 0
font_text = "0"

pipe_bool = False
pipe_index = 0

score = 0

# /////////////////////////////////////

setupBool = False
GameOverActivateBool = False
FinalGameOverBool = False

#
RestBtn = Classes.Button("graphics/Buttons/Restart.png", 400 - 125, 325)
RestBtn.Visible = False

MenuBtn = Classes.Button("graphics/Buttons/Menu.png", 400 + 125, 325)
MenuBtn.Visible = False

GOScreen = pygame.image.load("graphics/GameOver.png")
GOScreen_Rect = GOScreen.get_rect(center=(CENTER[0], CENTER[1] - 40))
GOScreen_Vis = False

GameOverFonts = pygame.font.Font("fonts/04B_19__.ttf", 45)
GOScore = GameOverFonts.render("1000", False, "White")
GOScore_rect = GOScore.get_rect(midleft=(CENTER[0] - 95, CENTER[1] + 5))
GOHighScr = GameOverFonts.render("1000", False, "White")
GoHighScr_rect = GOHighScr.get_rect(midleft=(CENTER[0] + 75, CENTER[1] + 5))

EasyBtn = Classes.Button("graphics/Buttons/EasyBtn.png", 400, 325 - 150)
MediBtn = Classes.Button("graphics/Buttons/MediumBtn.png", 400, 325 - 75)
HardBtn = Classes.Button("graphics/Buttons/HardBtn.png", 400, 325)
#

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
        font_rect2 = font_surface2.get_rect(center=(CENTER[0], CENTER[1] + 25))
        print(f'{pygame.time.get_ticks() - timer_splash}')

        if pygame.time.get_ticks() > timer_splash + 1000:
            if splash_ind == 0:
                score_sfx.play()
                splash_color = "white"
                timer_splash = pygame.time.get_ticks()
                splash_ind += 1
            else:
                ChangeScene(1)

        screen.fill("Black")
        screen.blit(font_surface, font_rect)
        screen.blit(font_surface2, font_rect2)

    if scene == 1:
        if setupBool == False:
            FlappELogo = pygame.image.load("graphics/Logo.png")
            FlappERect = FlappELogo.get_rect(center=(CENTER[0], CENTER[1] - 120))
            mixer.music.load("media/MenuTheme.mp3")
            mixer.music.play(-1)
            setupBool = True

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if EasyBtn.ButtonRect.collidepoint(e.pos):
                        save_data['game_mode'] = "Easy"
                        ChangeScene(2)
                    if MediBtn.ButtonRect.collidepoint(e.pos):
                        save_data['game_mode'] = "Medium"
                        ChangeScene(2)
                    if HardBtn.ButtonRect.collidepoint(e.pos):
                        save_data['game_mode'] = "Hard"
                        ChangeScene(2)

        screen.blit(BackGround_Surf, (0, 0))

        screen.blit(FlappELogo, FlappERect)
        EasyBtn.drawInScreen(screen)
        MediBtn.drawInScreen(screen)
        HardBtn.drawInScreen(screen)



    if scene == 2:
        if setupBool == False:
            Reset()
            debug_font = pygame.font.Font("fonts/Retro Gaming.ttf", 18)
            setupBool = True


        for e in events:
            if e.type == pipe_timer and gameEnd == False and gameStart:
                offset = random.randint(0, 150)
                pipe_group.add(Classes.Pipe("Upside", offset))
                pipe_group.add(Classes.Pipe("Downside", offset, gameModeData[save_data['game_mode'] + "_Gap"]))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if not gameStart:
                        gameStart = True
                    if gameEnd:
                        Reset()
                if e.key == pygame.K_ESCAPE:
                    ChangeScene(0)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if not gameStart:
                    gameStart = True
                    mixer.music.play(-1)

                if e.button == 1:
                    if RestBtn.ButtonRect.collidepoint(e.pos) and RestBtn.Visible:
                        print("Restart Clicked")
                        Reset()
                    if MenuBtn.ButtonRect.collidepoint(e.pos) and MenuBtn.Visible:
                        ChangeScene(1)
                        print("Menu Clicked")

        font_surface = font.render(font_text, False, 'White')
        font_rect = font_surface.get_rect(center=(CENTER[0], SCREEN_HEIGHT // 9))

        #
        debug_surface = splash_font.render(save_data['game_mode'], False, "Black")
        debug_rect = debug_surface.get_rect(midbottom=(0 + debug_surface.get_width(), screen.get_height()))
        #


        if gameEnd == False:
            font_text = str(score)
        else:
            if bird.sprites()[0].rect.y > 400:
                if not GameOverActivateBool:
                    GameOverTimer = pygame.time.get_ticks()
                    GameOverActivateBool = True


                if pygame.time.get_ticks() > GameOverTimer + 500:
                    FinalGameOverBool = True
                    MenuBtn.Visible = True
                    RestBtn.Visible = True
                    GOScreen_Vis = True
                    font_text = ""

                    if not gameOver_Played:
                        gameOver_sfx.play()
                        gameOver_Played = True


                else:
                    print(pygame.time.get_ticks() - GameOverTimer)


        if len(bird) > 0 and gameStart == False: bird.sprites()[0].rect.midbottom = (250, 225)

        if score > save_data[save_data['game_mode']+'_high_score']: save_data[save_data['game_mode']+'_high_score'] = score

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
        if gameActive:
            gameEnd = True
            mixer.music.stop()

        # ///////////////////////////////////

        pipe_group.draw(screen)
        pipe_group.update(gameActive)

        bird.draw(screen)
        bird.update(events, gameActive)

        screen.blit(font_surface, font_rect)
        # screen.blit(debug_surface, debug_rect)

        if GOScreen_Vis:
            GOScore = GameOverFonts.render(str(score), False, "White")
            GOHighScr = GameOverFonts.render(str(save_data[save_data['game_mode']+'_high_score']), False, "White")
            screen.blit(GOScreen, GOScreen_Rect)
            screen.blit(GOScore, GOScore_rect)
            screen.blit(GOHighScr, GoHighScr_rect)

        MenuBtn.update(screen, events, MenuBtn.Visible)
        RestBtn.update(screen, events, RestBtn.Visible)
        # ///////////////////////////////////

    pygame.display.update()
    clock.tick(60)
