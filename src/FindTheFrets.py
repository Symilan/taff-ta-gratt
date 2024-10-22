import pygame
from Constants import *
from DifficultyChoice import DifficultyChoice
import instrument
from Button import Button
from Scores import Highscores, Score
from utils import *
from Text import Text
from game import Game
class FindTheFrets(Game) :
    def __init__(self, max_round=MAX_ROUND, difficulty = Difficulty.EASY) :
        #Graphic
        Game.__init__(self)
        #Button
        self.validate_button = Button(VALIDATE_BUTTON_IMAGE, VALIDATE_BUTTON_HOVERED_IMAGE, image_greyed=VALIDATE_BUTTON_GREYED_IMAGE)
        self.validate_button.center().stick_to_bottom().shift(x=-20)
        #Game
        self.note_to_find = None

    def start() :
        state, difficulty = DifficultyChoice.start(States.FIND_THE_FRETS)
        game_instance = FindTheFrets(difficulty=difficulty)
        game_instance.start_round()
        while state == game_instance.get_supposed_state() :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                if event.type == pygame.KEYDOWN and event.key == 27 :
                    return States.HOME
                else :
                    state = game_instance.manage_event(event)
            game_instance.update()
            game_instance.display()
            pygame.display.update()
        return state

    def handle_validate(self) :
        if self.fretboard.selection_is_correct(self.note_to_find) :
            self.handle_correct()
        else :
            self.handle_incorrect()
    
    def choose_note(self) :
        previous_note = self.note_to_find
        while previous_note==self.note_to_find :
            if self.difficulty == Difficulty.EASY :
                self.note_to_find = instrument.Note.random_easy()
            else :
                self.note_to_find = instrument.Note.random()

    def handle_correct(self) :
        Game.handle_correct(self)
        self.text_rule.text = [
            "Bravo ! Tu as trouvé tous les "+str(self.note_to_find)+" !",
            "Clique n'importe où pour continuer."
        ]

    def handle_incorrect(self) :
        Game.handle_incorrect(self)
        self.text_rule.text = [
            "Raté ! Voici tous les "+str(self.note_to_find)+".", 
            "Clique n'importe où pour continuer."
        ]

    def update(self) :
        self.validate_button.is_active = self.fretboard.has_one_selection()

    def manage_play(self, event) :
        Game.manage_play(self, event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.validate_button.is_selected():
                self.handle_validate()
            for string in self.fretboard.strings :
                for fret in string.frets :
                    if fret.rect.collidepoint(pygame.mouse.get_pos()) :
                        fret.is_selected = not fret.is_selected
        return States.FIND_THE_FRETS

    def start_round(self) :
        Game.start_round(self)
        self.choose_note()
        self.fretboard.empty()
        self.text_rule.text = "Coche tous les "+str(self.note_to_find)+"."
        
    def display_play(self) :
        self.fretboard.draw(draw_hovered_frets=True)
        self.text_rule.write()
        self.validate_button.draw()

    def display_success(self) :
        self.fretboard.draw(draw_hovered_frets=False, write_selected_notes=True)
        self.text_rule.write()

    def display_failure(self) :
        self.fretboard.empty().check_all(self.note_to_find)
        self.fretboard.draw(draw_hovered_frets=False, write_selected_notes=True)
        self.text_rule.write()

    def get_supposed_state(self) :
        return States.FIND_THE_FRETS