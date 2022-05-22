import pygame
from pygame import mixer

mixer.init()
crash_sfx = mixer.Sound("media/Hit.mp3")
flapp_sfx = mixer.Sound("media/Flapp.mp3")



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mixer.music.load("media/NormalTheme.mp3")
        mixer.music.play(-1)

        bird_flapp1 = pygame.image.load("graphics/FlappE_1.png").convert_alpha()
        bird_flapp2 = pygame.image.load("graphics/FlappE_2.png").convert_alpha()
        bird_flapp3 = pygame.image.load("graphics/FlappE_3.png").convert_alpha()
        self.bird_flapp = [bird_flapp1, bird_flapp2, bird_flapp3, bird_flapp2]
        self.bird_index = 0

        self.bird_active = True
        self.crash_bool = False

        self.gravity = 2
        self.image = self.bird_flapp[self.bird_index]
        self.image = pygame.transform.scale(self.image, (51, 36))
        self.rect = self.image.get_rect(midbottom = (250, 100))

    def player_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and self.bird_active:
                if event.key == pygame.K_SPACE:
                    self.gravity = -6
                    flapp_sfx.stop()
                    flapp_sfx.play()

    def logic(self):
        self.rect.y += self.gravity
        self.gravity += 0.38
        if self.gravity > 10:
            self.gravity = 10

        if self.rect.bottom > 500:
            self.rect.bottom = 500

        #Crash sound bool
        if self.bird_active == False and self.crash_bool == False:
            crash_sfx.play()
            mixer.music.stop()
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
    def __init__(self, orientation, offset):
        super().__init__()
        if orientation == "Upside":
            self.image = pygame.image.load("graphics/PipeUpSide.png").convert_alpha()
            #750
            yPos = 600 + offset

        elif orientation == "Downside":
            self.image = pygame.image.load("graphics/PipeDownSide.png")
            #200
            yPos = 50 + offset

        self.image = pygame.transform.scale(self.image, (78 ,405))
        self.rect = self.image.get_rect(midbottom = (900 , yPos))

        self.pipe_active = True

        self.velocity = -5

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
