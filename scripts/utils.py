import os

import pygame

BASE_IMG_PATH = r'andmed/img/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(load_image(path + '/' + img_name))
    return images
 





