import pygame

w, h = 800, 600
rate = 64
clock = pygame.time.Clock()
win = pygame.display.set_mode((w, h))


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == 27):
            quit()
    win.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(rate)
