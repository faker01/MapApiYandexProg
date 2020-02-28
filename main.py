import pygame
import requests
from PIL import Image
from io import BytesIO


SCALE = 17
LON = 37.530887
LAT = 55.703118

w, h = 600, 450
rate = 64
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
    print(image.size)
    return image


def PIL_to_pygame(img):
    img = img.convert('RGB')
    return pygame.image.fromstring(img.tobytes("raw", 'RGB'), img.size, 'RGB')


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
