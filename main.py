import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
GAME_NAME = "PyGame"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME_NAME")
clock = pygame.time.Clock()

BackGround_Surf = pygame.image.load("graphics/BackGround_1.png").convert()

Flapp_Gravity = -10

Flapp_Surf = pygame.image.load("graphics/FlappE_1.png").convert_alpha()
Flapp_Surf = pygame.transform.scale(Flapp_Surf, (51, 36))
Flapp_Rect = Flapp_Surf.get_rect(midbottom=(50, 50))
Flapp_Sprites = ["graphics/FlappE_1.png", "graphics/FlappE_2.png", "graphics/FlappE_3.png"]
Flapp_Sprites_Index = 0

def Flapp_Anim(Flapp_Sprites_Index):

    Flapp_Surf = pygame.image.load(Flapp_Sprites[Flapp_Sprites_Index]).convert_alpha()
    Flapp_Sprites_Index += 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Flapp_Gravity = 7

    screen.blit(BackGround_Surf, (0,0))

    screen.blit(Flapp_Surf, Flapp_Rect)
    Flapp_Rect.y -= Flapp_Gravity
    Flapp_Gravity -= 0.35

    pygame.set

    if Flapp_Gravity < -10:
        Flapp_Gravity = -10

    if Flapp_Rect.y > 350:
        Flapp_Rect.y = 350
    pygame.display.update()
    clock.tick(60)






