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


class FlappEPlayer:
    def __init__(self):
        self.Flapp_Gravity = -10
        self.Flapp_Sprites = []
        self.Flapp_Sprites.append(pygame.image.load("graphics/FlappE_1.png").convert_alpha())
        self.Flapp_Sprites.append(pygame.image.load("graphics/FlappE_2.png").convert_alpha())
        self.Flapp_Sprites.append(pygame.image.load("graphics/FlappE_3.png").convert_alpha())
        self.Flapp_Sprites.append(pygame.image.load("graphics/FlappE_2.png").convert_alpha())
        self.Flapp_SprIndex = 0

        self.Flapp_Surf = self.Flapp_Sprites[self.Flapp_SprIndex]
        self.Flapp_Surf = pygame.transform.scale(self.Flapp_Surf, (51, 36))
        self.Flapp_Rect = self.Flapp_Surf.get_rect(midbottom=((screen.get_width() / 2) - (self.Flapp_Surf.get_width() / 2) + 20, 100))

    def updateSprite(self):
        self.Flapp_SprIndex += 0.15

        if self.Flapp_SprIndex >= len(self.Flapp_Sprites):
            self.Flapp_SprIndex = 0

        self.Flapp_Surf = self.Flapp_Sprites[int(self.Flapp_SprIndex)]
        self.Flapp_Surf = pygame.transform.scale(self.Flapp_Surf, (51, 36))


Flapp = FlappEPlayer()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Flapp.Flapp_Gravity = 7

    screen.blit(BackGround_Surf, (0, 0))

    screen.blit(Flapp.Flapp_Surf, Flapp.Flapp_Rect)
    Flapp.Flapp_Rect.y -= Flapp.Flapp_Gravity
    Flapp.Flapp_Gravity -= 0.35

    if Flapp.Flapp_Gravity < -10:
        Flapp.Flapp_Gravity = -10

    if Flapp.Flapp_Rect.y > 350:
        Flapp.Flapp_Rect.y = 350

    Flapp.updateSprite()

    pygame.display.update()
    clock.tick(60)






