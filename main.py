import pygame

class ImageButton:
    def __init__(self, path: str, position: tuple[int], callback):
        self.image: pygame.image = pygame.image.load(path)
        self.rect: pygame.Rect = self.image.get_rect(topleft=position)
        self.callback = callback

    def on_click(self, event: pygame.event.Event):
        if event.button == 1 and self.rect.collidepoint(event.pos): self.callback()

def testcallback():
    print("Hello world")

# noinspection SpellCheckingInspection
def main():
    pygame.init()

    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Power Fix")
    pygame.display.flip()

    background: pygame.image = pygame.image.load("assets/textures/backgroundEmpty.png")
    font: pygame.font = pygame.font.Font("assets/ui/Font/Kenney Future.ttf", 64)

    playbutton: ImageButton = ImageButton("assets/ui/Vector/Grey/button_rectangle_border.svg", (10, 10), testcallback)

    running: bool = True
    while running:
        background = pygame.transform.scale(background, pygame.display.get_window_size())
        playbutton.image = pygame.transform.scale(playbutton.image, (pygame.display.get_surface().get_width() / 4.4444, pygame.display.get_surface().get_height() / 7.5))

        pygame.display.get_surface().blit(background, (0 ,0))
        pygame.display.get_surface().blit(playbutton.image, playbutton.rect)

        titletext: pygame.Surface = font.render("Power Fix", 0, (30, 30, 30))
        pygame.display.get_surface().blit(titletext, (pygame.display.get_surface().get_width() // 2 - titletext.get_width() // 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11: pygame.display.set_mode((1280, 720), pygame.RESIZABLE) if bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN) else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                playbutton.on_click(event)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
