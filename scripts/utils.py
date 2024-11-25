'''import os

import pygame

BASE_IMG_PATH = 'andmed/img/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(load_image(path + '/' + img_name))
            return images'''

'''import os
import pygame

# Adjust the base path to point to the root directory of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMG_PATH = os.path.join(os.path.dirname(PROJECT_ROOT, 'andmed', 'img'))

def load_image(path):
    full_path = os.path.join(BASE_IMG_PATH, path)
    print(f"Attempting to load: {full_path}")  # Debug print
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    img = pygame.image.load(full_path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    dir_path = os.path.join(BASE_IMG_PATH, path)
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    for img_name in sorted(os.listdir(dir_path)):
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(load_image(os.path.join(path, img_name)))
    return images'''
import os
import pygame

# absoluuttee
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMG_PATH = os.path.join(PROJECT_ROOT, 'andmed', 'img')

def load_image(path):
    full_path = os.path.normpath(os.path.join(BASE_IMG_PATH, path))
    print(f"Attempting to load: {full_path}")  # praegu jääb, silumiseks
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")
    img = pygame.image.load(full_path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    dir_path = os.path.normpath(os.path.join(BASE_IMG_PATH, path))
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    for img_name in sorted(os.listdir(dir_path)):
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(load_image(os.path.join(path, img_name)))
    return images


 







