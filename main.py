import pygame
import requests
from PIL import Image
from io import BytesIO


SCALE = 17
LON = 37.530887
LAT = 55.703118

w, h = 600, 450
rate = 32
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((w, h))


def search_map(longitude, lattitude, delta):
    req = 'https://static-maps.yandex.ru/1.x/?ll={},{}&z={}&l=map'.format(longitude, lattitude,
                                                                               delta)
    response = requests.get(req)
    return response.content


def get_img_from_response(content):
    image = Image.open(BytesIO(content))
    return image


def PIL_to_pygame(img):
    img = img.convert('RGB')
    return pygame.image.fromstring(img.tobytes("raw", 'RGB'), img.size, 'RGB')


def get_map():
    response = search_map(LON, LAT, SCALE)
    pil_image = get_img_from_response(response)
    map_image = PIL_to_pygame(pil_image)
    return map_image

MAP = get_map()


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                quit()
            if e.key == pygame.K_PAGEUP:
                SCALE = min(17, SCALE + 1)
            if e.key == pygame.K_PAGEDOWN:
                SCALE = max(0, SCALE - 1)
            if e.key == pygame.K_LEFT:
                LON = (LON - 0.0005 * (18 - SCALE)) % 360
            if e.key == pygame.K_RIGHT:
                LON = (LON + 0.0005 * (18 - SCALE)) % 360
            if e.key == pygame.K_UP:
                LAT = (LAT + 0.0005 * (18 - SCALE)) % 360
            if e.key == pygame.K_DOWN:
                LAT = (LAT - 0.0005 * (18 - SCALE)) % 360
            MAP = get_map()

    win.fill((0, 0, 0))
    win.blit(MAP, (0, 0))
    pygame.display.flip()
    clock.tick(rate)
