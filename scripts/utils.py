import pygame
import os

#BASE_IMG_PATH = r'game-attempt\andmed\img'
#создает путь картинки
BASE_IMG_PATH = os.path.abspath(os.path.join('game-attempt', 'andmed', 'img'))


def load_image(path):
    full_path = os.path.join(BASE_IMG_PATH, path)
    img = pygame.image.load(full_path).convert()
    img.set_colorkey((0, 0, 0))
    return img

#for tiles
def load_images(path):
    images = []
    dir_path = os.path.join(BASE_IMG_PATH, path)
    for name in os.listdir(dir_path):
        if name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            full_path = os.path.join(path, name)
            images.append(load_image(full_path))
    return images



