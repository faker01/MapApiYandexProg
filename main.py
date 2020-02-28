import pygame
import requests
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


def search_map(longitude, lattitude, delta):
    req = 'https://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l=map'.format(longitude, lattitude,
                                                                               delta, delta)
    response = requests.get(req)
    return response.content


def get_img_from_response(content):
    image = Image.open(BytesIO(content))
    return image


def PIL_to_pygame(img):
    print(img.getpixel((0, 0)))
    return pygame.image.fromstring(img.tobytes("raw", 'P'), img.size, 'P')


# micro mainloop
response = search_map(LON, LAT, SCALE)
pil_image = get_img_from_response(response)
map_image = PIL_to_pygame(pil_image)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            quit()
    win.fill((0, 0, 0))
    win.blit(map_image, (0, 0))
    pygame.display.flip()
    clock.tick(rate)
