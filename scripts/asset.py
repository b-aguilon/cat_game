import pygame
import os

IMAGE_PATH = 'assets/img/'

assets = {}
tiles = []

def load_assets():
    if len(assets) != 0 or len(tiles) != 0:
        raise Exception('assets already loaded')

    assets.update({
        'road' : load_images('tiles/road'),
        'ramp' : load_images('tiles/ramp'),
        'cat' : load_image('entities/player/cat.png')
    })

def load_image(path):
    img = pygame.image.load(IMAGE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    if path.startswith('tiles/'):
        path_parts = path.split('/')
        tiles.append(path_parts[1])
    for img_name in sorted(os.listdir(IMAGE_PATH + path)):
        images.append(load_image(path + '/' + img_name))    
    return images