import pygame
from Constants import *

def load_image(image, scale = 1) :
    image = pygame.image.load(image)
    width = image.get_width()
    height = image.get_height()
    image = pygame.transform.scale(image, (int(scale*width), int(scale*height)))
    return image