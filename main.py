import pygame

def main():
    pygame.init()

    pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Power Fix")
    pygame.display.flip()

    background: pygame.image = pygame.transform.scale(pygame.image.load("assets/textures/backgroundEmpty.png"), (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))

    running: bool = True
    while running:
        pygame.display.get_surface().blit(background, (0 ,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        pygame.display.update()

if __name__ == '__main__':
    main()
