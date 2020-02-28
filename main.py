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
types_of_map = ['map', 'sat', ','.join(['sat', 'skl'])]
current_map = 0


def search_map(longitude, lattitude, delta):
    params = {'ll': ','.join([str(longitude), str(lattitude)]),
              'z': str(delta),
              'l': types_of_map[current_map]}
    req = 'https://static-maps.yandex.ru/1.x/'
    response = requests.get(req, params=params)
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_PAGEUP:
                SCALE = min(17, SCALE + 1)
            if event.key == pygame.K_PAGEDOWN:
                SCALE = max(0, SCALE - 1)
            if event.key == pygame.K_LEFT:
                LON = (LON - 0.0005 * (18 - SCALE)) % 360
            if event.key == pygame.K_RIGHT:
                LON = (LON + 0.0005 * (18 - SCALE)) % 360
            if event.key == pygame.K_UP:
                LAT = (LAT + 0.0005 * (18 - SCALE)) % 360
            if event.key == pygame.K_DOWN:
                LAT = (LAT - 0.0005 * (18 - SCALE)) % 360
            if event.key == pygame.K_SPACE:
                current_map += 1
                current_map %= 3
            MAP = get_map()

    win.fill((0, 0, 0))
    win.blit(MAP, (0, 0))
    pygame.display.flip()
    clock.tick(rate)
