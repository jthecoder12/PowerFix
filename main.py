"""
Power Fix
Author: jthecoder12
A submission to the Kenney Jam 2025
"""

import pygame
from pygame import mixer
from random import randint

playing: bool = False

class ImageButton:
    def __init__(self, path: str, position: tuple[int], callback):
        self.image: pygame.Surface = pygame.image.load(path)
        self.rect: pygame.Rect = self.image.get_rect(topleft=position)
        self.callback = callback

    def on_click(self, event: pygame.event.Event):
        if event.button == 1 and self.rect.collidepoint(event.pos): self.callback()

    def resize(self, position: tuple[int]): self.rect = self.image.get_rect(topleft=position)

class Player:
    def __init__(self):
        self.image: pygame.Surface = pygame.image.load("assets/textures/extra_character_a.svg")
        self.position: tuple[int] = (pygame.display.get_surface().get_width() / 2 - self.image.get_width() / 2, pygame.display.get_surface().get_height() / 2 - self.image.get_height() / 2)
        self.speed = pygame.display.get_surface().get_width() / 1280

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.position)

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        x, y = self.position
        if keys[pygame.K_w]: y -= self.speed
        if keys[pygame.K_s]: y += self.speed
        if keys[pygame.K_a]: x -= self.speed
        if keys[pygame.K_d]: x += self.speed

        self.position = (x, y)

    def updatespeed(self):
        self.speed = pygame.display.get_surface().get_width() / 1280

class Machine:
    def __init__(self, position: tuple[int]):
        self.image: pygame.Surface = pygame.image.load("assets/textures/block_large.png")
        self.position: tuple[int] = position

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.position)

    def touchingplayer(self, player: Player) -> bool: return self.image.get_rect(topleft=self.position).collidepoint(player.position[0] + player.image.get_width() / 2, player.position[1] + player.image.get_height() / 2)

class Battery:
    def __init__(self):
        self.image: pygame.Surface = pygame.image.load("assets/textures/brick_high_1.svg")
        self.position: tuple[int] = (randint(0, pygame.display.get_surface().get_width()), randint(0, pygame.display.get_surface().get_height()))

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.position)

    def touchingplayer(self, player: Player) -> bool: return self.image.get_rect(topleft=self.position).collidepoint(player.position[0] + player.image.get_width() / 2, player.position[1] + player.image.get_height() / 2)

def playcallback():
    global playing
    mixer.Sound("assets/ui/Sounds/click-b.ogg").play()
    playing = True


# noinspection SpellCheckingInspection,PyUnboundLocalVariable
def main():
    global playing

    pygame.init()
    mixer.init()

    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Power Fix")
    pygame.display.flip()

    background: pygame.Surface = pygame.image.load("assets/textures/backgroundEmpty.png")
    font: pygame.font.Font = pygame.font.Font("assets/ui/Font/Kenney Future.ttf", 64)
    smallerfont: pygame.font.Font = pygame.font.Font("assets/ui/Font/Kenney Future.ttf", 32)

    playbutton: ImageButton = ImageButton("assets/ui/Vector/Grey/button_rectangle_border.svg", (pygame.display.get_surface().get_width() / 2 - pygame.display.get_surface().get_width() / 8.8888, 150), playcallback)

    player: Player = Player()

    currentbattery: Battery = Battery()
    hasbattery: bool = False

    machine1: Machine = Machine((0, 0))
    machinewidth: int = machine1.image.get_width()
    machineheight: int = machine1.image.get_height()
    machine2: Machine = Machine((pygame.display.get_surface().get_width() - machinewidth, 0))
    machine3: Machine = Machine((0, pygame.display.get_surface().get_height() - machineheight))
    machine4: Machine = Machine((machine2.position[0], machine3.position[1]))

    score: int = 0

    mixer.music.load("assets/sounds/Chill.wav")
    mixer.music.play(-1)

    dropsound: mixer.Sound = mixer.Sound("assets/sounds/coin_drop.ogg")

    running: bool = True
    while running:
        background = pygame.transform.scale(background, pygame.display.get_window_size())
        pygame.display.get_surface().blit(background, (0, 0))

        if playing:
            currentbattery.render(pygame.display.get_surface())

            machine2.position = (pygame.display.get_surface().get_width() - machinewidth, 0)
            machine3.position = (0, pygame.display.get_surface().get_height() - machineheight)
            machine4.position = (machine2.position[0], machine3.position[1])
            machines: list[Machine] = [machine1, machine2, machine3, machine4]
            for machine in machines: machine.render(pygame.display.get_surface())

            player.render(pygame.display.get_surface())

            pygame.display.get_surface().blit(smallerfont.render(f"Score: {score}", 0, (30, 30, 30)), (0, 0))
        else:
            playbutton.image = pygame.transform.scale(playbutton.image, (pygame.display.get_surface().get_width() / 4.4444, pygame.display.get_surface().get_height() / 7.5))
            pygame.display.get_surface().blit(playbutton.image, playbutton.rect)

            titletext: pygame.Surface = font.render("Power Fix", 0, (30, 30, 30))
            pygame.display.get_surface().blit(titletext, (pygame.display.get_surface().get_width() / 2 - titletext.get_width() / 2, 10))

            playtext: pygame.Surface = font.render("Play", 0, (30, 30, 30))
            pygame.display.get_surface().blit(playtext, (pygame.display.get_surface().get_width() / 2 - playtext.get_width() / 2, 150 + playbutton.rect.height / 4))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.set_mode((1280, 720), pygame.RESIZABLE) if bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN) else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    playbutton.resize((pygame.display.get_surface().get_width() / 2 - pygame.display.get_surface().get_width() / 8.8888,150))
                elif event.key == pygame.K_p and currentbattery.touchingplayer(player) and not hasbattery:
                    hasbattery = True
                    currentbattery = Battery()

                if playing:
                    if event.key == pygame.K_ESCAPE:
                        score = 0
                        hasbattery = False
                        player.position = (pygame.display.get_surface().get_width() / 2 - player.image.get_width() / 2, pygame.display.get_surface().get_height() / 2 - player.image.get_height() / 2)
                        playing = False

                    for machineA in machines:
                        if event.key == pygame.K_SPACE and machineA.touchingplayer(player) and hasbattery:
                            dropsound.play()
                            hasbattery = False
                            score += 1
                elif event.key == pygame.K_ESCAPE:
                    mixer.quit()
                    pygame.quit()
                    exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not playing: playbutton.on_click(event)
            elif event.type == pygame.WINDOWRESIZED:
                if playing: player.updatespeed()
                else: playbutton.resize((pygame.display.get_surface().get_width() / 2 - pygame.display.get_surface().get_width() / 8.8888, 150))

        pygame.display.update()

    mixer.quit()
    pygame.quit()

if __name__ == '__main__':
    main()
