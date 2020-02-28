import pygame
from PIL import Image
from io import BytesIO


SCALE = 0.002
LON = 37.530887
LAT = 55.703118

w, h = 800, 600
rate = 64
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((w, h))


def get_img_from_respone(content):
    image = Image.open(BytesIO(content))
    return image


def PIL_to_pygame(img):
    return pygame.image.fromstring(img.tobytes("raw", 'RGB'), img.size, 'RGB')


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            quit()
    win.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(rate)
