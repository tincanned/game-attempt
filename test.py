import pygame
pygame.init()
try:
    img = pygame.image.load(r'game-attempt\data\img\large_decor\large_decor2.png')

    print("Image loaded successfully")
except pygame.error as e:
    print(f"Failed to load image: {e}")
