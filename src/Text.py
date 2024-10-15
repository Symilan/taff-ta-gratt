import pygame

from Constants import BASIC_SHIFT, FRETBOARD_SCALING

class Text :
    pygame.font.init()
    my_font = pygame.font.Font("src/ressources/PixelifySans-Regular.ttf", 50)
    def __init__(self, text="", coordinates=(0,0), color=(0,0,0)) :
        self.text = text
        self.coordinates = coordinates
        self.color = color
    
    def set_coordinates(self, coordinates) :
        if isinstance(coordinates, pygame.Surface) :
            print("Je suis une Surface, pas une coordonée")
            print("Coord : "+str(self.coordinates)+" Surface : "+str(coordinates))
        self.coordinates = coordinates

    def get_surface(self) :
        return Text.my_font.render(self.text, False, self.color)
    
    def get_rect(self) :
        rect = self.get_surface().get_rect()
        rect.topleft = self.coordinates
        return rect

    def write(self) :
        if isinstance(self.text, str) :
            text_surface = self.get_surface()
            pygame.display.get_surface().blit(text_surface, self.coordinates)
        elif isinstance(self.text, list) :
            x,y = self.coordinates
            for line in self.text :
                text_surface = Text.my_font.render(line, False, self.color)
                pygame.display.get_surface().blit(text_surface, (x,y))
                y += text_surface.get_height()
        return self

    def center_on_rect(self, rect) :
        text_rect = self.get_rect()
        text_rect.center = rect.center

        #Je ne sais pas pourquoi il faut rectifier comme ça
        text_rect.top -= int(FRETBOARD_SCALING/2)-1
        text_rect.left += int(FRETBOARD_SCALING/2)

        self.set_coordinates(text_rect.topleft)
        return self

    def stick_to_top(self, shift=BASIC_SHIFT) :
        rect = self.get_rect()
        rect.top = pygame.display.get_surface().get_rect().top+shift
        self.set_coordinates(rect.topleft)
        return self
    
    def stick_to_right(self, shift=BASIC_SHIFT) :
        rect = self.get_rect()
        rect.right = pygame.display.get_surface().get_rect().right-shift
        self.set_coordinates(rect.topleft)
        return self
    
    def stick_to_left(self, shift=BASIC_SHIFT) :
        rect = self.get_rect()
        rect.left = shift
        self.set_coordinates(rect.topleft)
        return self
    
    def centerx(self, shift = 0) :
        rect = self.get_rect()
        rect.centerx = pygame.display.get_surface().get_rect().centerx
        self.set_coordinates(rect.topleft)
        return self