import pygame
from pygame import mixer

mixer.init()
crash_sfx = mixer.Sound("media/Hit.mp3")
flapp_sfx = mixer.Sound("media/Flapp.mp3")



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        bird_flapp1 = pygame.image.load("graphics/FlappE_1.png").convert_alpha()
        bird_flapp2 = pygame.image.load("graphics/FlappE_2.png").convert_alpha()
        bird_flapp3 = pygame.image.load("graphics/FlappE_3.png").convert_alpha()
        self.bird_flapp = [bird_flapp1, bird_flapp2, bird_flapp3, bird_flapp2]
        self.bird_index = 0

        self.bird_active = True
        self.crash_bool = False
        self.gameStart = False

        self.gravity = 0
        self.image = self.bird_flapp[self.bird_index]
        self.image = pygame.transform.scale(self.image, (51, 36))
        self.rect = self.image.get_rect(midbottom = (250, 175))

    def player_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and self.bird_active:
                if event.key == pygame.K_SPACE:
                    self.gravity = -6
                    self.gameStart = True
                    flapp_sfx.stop()
                    flapp_sfx.play()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.bird_active:
                self.gravity = -6
                self.gameStart = True
                flapp_sfx.stop()
                flapp_sfx.play()

    def logic(self):
        self.rect.y += self.gravity
        if self.gameStart: self.gravity += 0.38

        if self.gravity > 10:
            self.gravity = 10

        if self.rect.top < 0:
            self.rect.top = 0
            self.gravity = 0

        if self.rect.bottom > 600:
            self.rect.bottom = 600

        #Crash sound bool
        if self.bird_active == False and self.crash_bool == False:
            crash_sfx.play()
            mixer.music.pause()
            self.crash_bool = True

    def animation(self):
        self.bird_index += 0.15
        if self.bird_index > len(self.bird_flapp):
            self.bird_index = 0

        self.image = self.bird_flapp[int(self.bird_index)]
        self.image = pygame.transform.scale(self.image, (51, 36))

    def checkCollision(self, collision):
        if collision:
            self.bird_active = False


    def score(self):
        if self.rect.x > Pipe.rect.x:
            return 1

    def update(self, events, collision):
        self.player_input(events)
        self.logic()
        self.animation()
        self.checkCollision(collision)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, orientation, offset, gap = 0):
        super().__init__()
        if orientation == "Upside":
            self.image = pygame.image.load("graphics/PipeUpSide.png").convert_alpha()
            #750
            yPos = 600 + offset

        elif orientation == "Downside":
            self.image = pygame.image.load("graphics/PipeDownSide.png")
            #200
            yPos = 200 + offset - gap

        self.image = pygame.transform.scale(self.image, (78 ,405))
        self.rect = self.image.get_rect(midbottom = (900 , yPos))

        self.pipe_active = True

        self.velocity = -4

    def logic(self):
        if self.pipe_active:
            self.rect.x += self.velocity

        if self.rect.x < -100:
            self.kill()

    def checkCollision(self, gameActive):
        if gameActive:
            self.pipe_active = False

    def update(self, gameActive):
        self.logic()
        self.checkCollision(gameActive)


class Button():
    def __init__(self, image, x, y, onClick="", optImage=""):
        super().__init__()
        self.NormalButton = pygame.image.load(image).convert_alpha()
        self.ButtonRect = self.NormalButton.get_rect(center=(x, y))
        if len(onClick) > 0:
            self.onClickFunct = onClick
        else:
            self.onClickFunct = print(f"No Function Addeed [ImageRef:{image}]")
        if len(optImage) > 0:
            self.OptButton = pygame.image.load(optImage).convert_alpha()


    def checkInput(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.ButtonRect.collidepoint(e.pos):
                        print("MouseClicked")



    def drawInScreen(self, screen):
        screen.blit(self.NormalButton, self.ButtonRect)

    def update(self, screen, events, visible):
        if visible:
            self.checkInput(events)
            self.drawInScreen(screen)
