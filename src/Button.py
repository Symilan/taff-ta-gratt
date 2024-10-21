import pygame
from Constants import *

class Button :
    def __init__(self, image, image_hovered, image_greyed = None, coords = (0, 0)) :
        self.image = image
        self.image_hovered = image_hovered
        self.image_greyed = image_greyed
        self.is_active = True
        self.rect = self.image.get_rect()
        self.rect.topleft = coords

    def center(self) :
        self.rect.center = pygame.display.get_surface().get_rect().center
        return self

    def shift(self, x=0, y=0) :
        self.rect.top += x
        self.rect.left += y
        return self

    def stick_to_bottom(self) :
        self.rect.bottom = pygame.display.get_surface().get_rect().bottom
        return self
    
    def stick_to_left(self, shift = BASIC_SHIFT) :
        self.rect.left = pygame.display.get_surface().get_rect().left + shift
        return self

    def stick_to_right(self, shift = BASIC_SHIFT) :
        self.rect.right = pygame.display.get_surface().get_rect().right - shift
        return self

    def exit_button(image, hovered_image) :
        pass

    def is_hovered(self) :
        mousePos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mousePos)
    
    def is_selected(self) :
        return self.is_hovered() and self.is_active
    
    def draw (self) :
        screen = pygame.display.get_surface()
        if not(self.is_active) :
            screen.blit(self.image_greyed, (self.rect.topleft))
        elif self.is_hovered():
            screen.blit(self.image_hovered, (self.rect.topleft))
        else :
            screen.blit(self.image, ((self.rect.x, self.rect.y)))