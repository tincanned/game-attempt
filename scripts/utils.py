
import os
import pygame


BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '../andmed/img')

def load_image(path):
    
    full_path = os.path.join(BASE_IMG_PATH, path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image file not found: {full_path}")
    img = pygame.image.load(full_path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    full_path = os.path.join(BASE_IMG_PATH, path)
    if not os.path.isdir(full_path):
        raise FileNotFoundError(f"Directory not found: {full_path}")
    
    images = []
    for img_name in sorted(os.listdir(full_path)):
        if img_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(load_image(os.path.join(path, img_name)))
    return images



 







