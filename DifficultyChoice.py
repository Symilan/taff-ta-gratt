import pygame

from Button import Button
from Constants import *

class DifficultyChoice :
    def __init__(self) :
        self.easy_button = Button(EASY_BUTTON_IMAGE, EASY_BUTTON_HOVERED_IMAGE).center().shift(x=-100)
        self.hard_button = Button(HARD_BUTTON_IMAGE, HARD_BUTTON_HOVERED_IMAGE).center().shift(x=100)

    def start(game_state) -> States :
        difficulty_choice = DifficultyChoice()
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL, None
                if event.type == pygame.KEYDOWN and event.key == 27 :
                    return States.HOME, None
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                    if difficulty_choice.easy_button.is_selected() :
                        return game_state, Difficulty.EASY
                    elif difficulty_choice.hard_button.is_selected() :
                        return game_state, Difficulty.HARD
            difficulty_choice.display()
            pygame.display.update()
    
    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        self.easy_button.draw()
        self.hard_button.draw()