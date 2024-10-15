import pygame
from Constants import *
from DifficultyChoice import DifficultyChoice
from FretBoard import *
from Button import Button
from utils import *
from Text import Text

class FindTheNote :
    def __init__(self, max_round=10, difficulty = Difficulty.EASY) :
        #Graphic
        self.fretBoard = FretBoard()
        #Button
        self.validate_button = Button(VALIDATE_BUTTON_IMAGE, VALIDATE_BUTTON_HOVERED_IMAGE, image_greyed=VALIDATE_BUTTON_GREYED_IMAGE)
        self.validate_button.center().stick_to_bottom().shift(x=-20)
        #Text
        self.text_rule = Text(coordinates=QUESTION_COORDINATES)
        self.text_score = Text()
        self.text_round = Text()
        self.text_game_over = Text("Bien joué ! Partie terminée.").center_on_rect(pygame.display.get_surface().get_rect())
        #Game
        self.note_to_find = None
        self.state = FindTheNoteState.PLAY
        self.score = 0
        self.round_counter = 0
        self.max_round = max_round
        self.passed_notes = []
        self.difficulty = difficulty

    def handle_validate(self) :
        if self.fretBoard.selection_is_correct(self.note_to_find) :
            self.handle_correct()
        else :
            self.handle_incorrect()

    def handle_correct(self) :
        self.score += 1
        self.state = FindTheNoteState.SUCCESS
        self.text_rule.text = [
            "Bravo ! Tu as trouvé tous les "+str(self.note_to_find)+" !",
            "Clique n'importe où pour continuer."
        ]

    def handle_incorrect(self) :
        self.state = FindTheNoteState.FAILURE
        self.text_rule.text = [
            "Raté ! Voici tous les "+str(self.note_to_find)+".", 
            "Clique n'importe où pour continuer."
        ]

    def update(self) :
        self.validate_button.is_active = self.fretBoard.has_one_selection()
        self.text_score.text = "Score = "+str(self.score)
        self.text_round.text = "Round = "+str(self.round_counter)+"/"+str(self.max_round)

    def start() :
        state, difficulty = DifficultyChoice.start(States.FIND_THE_NOTE)
        findTheNote = FindTheNote(difficulty=difficulty)
        findTheNote.start_round()
        while state == States.FIND_THE_NOTE :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                if event.type == pygame.KEYDOWN and event.key == 27 :
                    state = States.HOME
                else :
                    state = findTheNote.manage_event(event)
            findTheNote.update()
            findTheNote.display()
            pygame.display.update()
        return state

    def manage_event(self, event) :
        match self.state :
            case FindTheNoteState.PLAY :
                return self.manage_play(event)
            case FindTheNoteState.SUCCESS :
                return self.manage_success(event)
            case FindTheNoteState.FAILURE :
                return self.manage_failure(event)
            case FindTheNoteState.GAME_OVER :
                return self.manage_game_over(event)

    def manage_play(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.validate_button.is_selected():
                self.handle_validate()
            for string in self.fretBoard.strings :
                for fret in string.frets :
                    if fret.rect.collidepoint(pygame.mouse.get_pos()) :
                        fret.is_selected = not fret.is_selected
        elif event.type == pygame.KEYDOWN and event.key == 32 :
            self.fretBoard.show_notes = not(self.fretBoard.show_notes)
        return States.FIND_THE_NOTE

    def manage_success(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round_counter >= self.max_round :
                self.state = FindTheNoteState.GAME_OVER
            else :
                self.start_round()
        return States.FIND_THE_NOTE

    def manage_failure(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round_counter >= self.max_round :
                self.state = FindTheNoteState.GAME_OVER
            else :
                self.start_round()
        return States.FIND_THE_NOTE
    
    def manage_game_over(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            return States.HOME
        return States.FIND_THE_NOTE

    def choose_note(self) :
        previous_note = self.note_to_find
        while previous_note==self.note_to_find :
            if self.difficulty == Difficulty.EASY :
                self.note_to_find = Note.random_easy()
            else :
                self.note_to_find = Note.random()

    def start_round(self) :
        self.choose_note()
        self.round_counter += 1
        self.passed_notes.append(self.note_to_find)
        self.state = FindTheNoteState.PLAY
        self.text_rule.text = "Coche tous les "+str(self.note_to_find)+"."
        self.fretBoard.empty()

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        match self.state :
            case FindTheNoteState.PLAY :
                self.display_play()
            case FindTheNoteState.SUCCESS :
                self.display_success()
            case FindTheNoteState.FAILURE :
                self.display_failure()
            case FindTheNoteState.GAME_OVER :
                self.display_game_over()
        text_round = self.text_round.stick_to_right().stick_to_top().write()
        text_round_bottom = text_round.get_rect().bottom
        self.text_score.stick_to_right().stick_to_top(text_round_bottom).write()

    def display_play(self) :
        self.fretBoard.draw(draw_hovered_frets=True)
        self.text_rule.write()
        self.validate_button.draw()


    def display_success(self) :
        self.fretBoard.draw(draw_hovered_frets=False, write_selected_notes=True)
        self.text_rule.write()

    def display_failure(self) :
        self.fretBoard.empty().check_all(self.note_to_find)
        self.fretBoard.draw(draw_hovered_frets=False, write_selected_notes=True)
        self.text_rule.write()

    def display_game_over(self) :
        self.text_game_over.write()
