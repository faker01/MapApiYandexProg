import pygame
import requests
from PIL import Image
from io import BytesIO
import Modules

SCALE = 10
LON = 0
LAT = 0
LON_marker = 0
LAT_marker = 0

w, h = 1050, 500
rate = 60

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((w, h))

types_of_map = ['map', 'sat', 'sat,skl']
current_map = 0
active = False

search_bar = Modules.InputBox(675, 25, 350, 32)
button_search = Modules.Button(675, 75, 350, 32, 'Искать')
button_clear = Modules.Button(675, 125, 350, 32, 'Сбросить')


def search_map(longitude, lattitude, longitude_marker, lattitude_marker, delta):
    params = {'ll': ','.join([str(longitude), str(lattitude)]),
              'z': str(delta),
              'l': types_of_map[current_map],
              'pt': ','.join([str(longitude_marker), str(lattitude_marker), 'pm2rdm'])}
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
    response = search_map(LON, LAT, LON_marker, LAT_marker, SCALE)
    pil_image = get_img_from_response(response)
    map_image = PIL_to_pygame(pil_image)
    return map_image


def get_coords(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"
    }
    try:
        json_response = requests.get(geocoder_api_server, params=geocoder_params).json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        return float(toponym_longitude), float(toponym_lattitude)
    except:
        return 0, 0


MAP = get_map()

while True:
    for event in pygame.event.get():
        
        if button_clear.handle_event(event):
            LON = 0
            LAT = 0
            LON_marker = 0
            LAT_marker = 0
            search_bar.text = ''
            MAP = get_map()
            
        if search_bar.handle_event(event):
            LON, LAT = get_coords(search_bar.text)
            LON_marker, LAT_marker = LON, LAT
            search_bar.text = ''
        search_bar.update()
        
        if button_search.handle_event(event):
            LON, LAT = get_coords(search_bar.text)
            LON_marker, LAT_marker = LON, LAT
            search_bar.text = ''
            MAP = get_map()
            
        if event.type == pygame.QUIT:
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            elif event.key == pygame.K_PAGEUP:
                SCALE = min(17, SCALE + 1)
            elif event.key == pygame.K_PAGEDOWN:
                SCALE = max(0, SCALE - 1)
            elif event.key == pygame.K_LEFT:
                LON = (LON - 0.0005 * (18 - SCALE)) % 360
            elif event.key == pygame.K_RIGHT:
                LON = (LON + 0.0005 * (18 - SCALE)) % 360
            elif event.key == pygame.K_UP:
                LAT = (LAT + 0.0005 * (18 - SCALE)) % 360
            elif event.key == pygame.K_DOWN:
                LAT = (LAT - 0.0005 * (18 - SCALE)) % 360
            elif event.key == pygame.K_INSERT:
                current_map += 1
                current_map %= 3
                
            MAP = get_map()

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (155, 155, 155), pygame.Rect(0, 0, 650, 500))
    win.blit(MAP, (25, 25))
    pygame.draw.rect(win, (250, 250, 250), pygame.Rect(650, 0, 400, 500))

    search_bar.draw(win)
    button_clear.draw(win)
    button_search.draw(win)

    pygame.display.flip()
    clock.tick(rate)
