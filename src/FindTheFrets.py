import pygame
from Constants import *
from DifficultyChoice import DifficultyChoice
from FretBoard import *
from Button import Button
from Scores import Highscores, Score
from utils import *
from Text import Text

class FindTheFrets :
    def __init__(self, max_round=FIND_THE_FRETS_MAX_ROUNDS, difficulty = Difficulty.EASY) :
        #Graphic
        self.fretBoard = FretBoard()
        #Button
        self.validate_button = Button(VALIDATE_BUTTON_IMAGE, VALIDATE_BUTTON_HOVERED_IMAGE, image_greyed=VALIDATE_BUTTON_GREYED_IMAGE)
        self.validate_button.center().stick_to_bottom().shift(x=-20)
        #Text
        self.text_rule = Text(coordinates=QUESTION_COORDINATES)
        self.text_score = Text()
        self.text_round = Text()
        self.text_timer = Text()
        self.text_game_over = Text("Bien joué ! Partie terminée.").center_on_rect(pygame.display.get_surface().get_rect())
        #Game
        self.note_to_find = None
        self.state = InGameState.PLAY
        self.won_rounds = 0
        self.round_counter = 0
        self.max_round = max_round
        self.passed_notes = []
        self.difficulty = difficulty
        self.timer = 0
        self.highscores = Highscores()
        self.highlighted_score_index = -1

    def start() :
        state, difficulty = DifficultyChoice.start(States.FIND_THE_FRETS)
        find_the_frets = FindTheFrets(difficulty=difficulty)
        find_the_frets.start_round()
        while state == States.FIND_THE_FRETS :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    return States.KILL
                if event.type == pygame.KEYDOWN and event.key == 27 :
                    state = States.HOME
                else :
                    state = find_the_frets.manage_event(event)
            find_the_frets.update()
            find_the_frets.display()
            pygame.display.update()
        return state

    def handle_validate(self) :
        if self.fretBoard.selection_is_correct(self.note_to_find) :
            self.handle_correct()
        else :
            self.handle_incorrect()

    def get_timer_str(self) -> str :
        total_seconds = int(self.timer/10)
        minutes = int(total_seconds/60)
        seconds = total_seconds % 60
        return str(minutes)+":"+str(seconds)

    def get_timer_total_seconds(self) -> int :
        return int(self.timer/10)
    
    def choose_note(self) :
        previous_note = self.note_to_find
        while previous_note==self.note_to_find :
            if self.difficulty == Difficulty.EASY :
                self.note_to_find = Note.random_easy()
            else :
                self.note_to_find = Note.random()

    def handle_correct(self) :
        self.won_rounds += 1
        self.state = InGameState.SUCCESS
        self.text_rule.text = [
            "Bravo ! Tu as trouvé tous les "+str(self.note_to_find)+" !",
            "Clique n'importe où pour continuer."
        ]

    def handle_incorrect(self) :
        self.state = InGameState.FAILURE
        self.text_rule.text = [
            "Raté ! Voici tous les "+str(self.note_to_find)+".", 
            "Clique n'importe où pour continuer."
        ]

    def update(self) :
        self.validate_button.is_active = self.fretBoard.has_one_selection()
        self.text_score.text = "Score = "+str(self.won_rounds)
        self.text_round.text = "Round = "+str(self.round_counter)+"/"+str(self.max_round)
        self.text_timer.text = self.get_timer_str()

    def manage_event(self, event) :
        match self.state :
            case InGameState.PLAY :
                return self.manage_play(event)
            case InGameState.SUCCESS :
                return self.manage_success(event)
            case InGameState.FAILURE :
                return self.manage_failure(event)
            case InGameState.GAME_OVER :
                return self.manage_game_over(event)

    def manage_play(self, event) :
        if event.type == TENTHSECOND_EVENT :
            self.timer += 1
            return States.FIND_THE_FRETS
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.validate_button.is_selected():
                self.handle_validate()
            for string in self.fretBoard.strings :
                for fret in string.frets :
                    if fret.rect.collidepoint(pygame.mouse.get_pos()) :
                        fret.is_selected = not fret.is_selected
        elif event.type == pygame.KEYDOWN and event.key == 32 :
            self.fretBoard.show_notes = not(self.fretBoard.show_notes)
        return States.FIND_THE_FRETS

    def manage_success(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round_counter >= self.max_round :
                self.enter_game_over()
            else :
                self.start_round()
        return States.FIND_THE_FRETS

    def manage_failure(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round_counter >= self.max_round :
                self.enter_game_over()
            else :
                self.start_round()
        return States.FIND_THE_FRETS
    
    def enter_game_over(self) :
        self.state = InGameState.GAME_OVER
        score = Score(self.won_rounds, self.get_timer_total_seconds())
        self.highlighted_score_index = self.highscores.add(score)

    def manage_game_over(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            return States.HOME
        return States.FIND_THE_FRETS

    def start_round(self) :
        self.choose_note()
        self.round_counter += 1
        self.passed_notes.append(self.note_to_find)
        self.state = InGameState.PLAY
        self.text_rule.text = "Coche tous les "+str(self.note_to_find)+"."
        self.fretBoard.empty()

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        match self.state :
            case InGameState.PLAY :
                self.display_play()
            case InGameState.SUCCESS :
                self.display_success()
            case InGameState.FAILURE :
                self.display_failure()
            case InGameState.GAME_OVER :
                self.display_game_over()
        text_round = self.text_round.stick_to_right().stick_to_top().write()
        text_round_bottom = text_round.get_rect().bottom
        text_score = self.text_score.stick_to_right().stick_to_top(text_round_bottom).write()
        text_score_bottom = text_score.get_rect().bottom
        self.text_timer.stick_to_right().stick_to_top(text_score_bottom).write()

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
        text_surfaces = []
        text_surfaces.append(Text("Highscores :").get_surface())
        for i in range(len(self.highscores.list)) :
            color = BLACK
            if i == self.highlighted_score_index :
                color = RED
            text_surfaces.append(Text(str(self.highscores.list[i]), color=color).get_surface())
        height = 0
        width = 0
        for text_surface in text_surfaces :
            height += text_surface.get_rect().height
            width = max(width, text_surface.get_rect().width)
        total_text_surface = pygame.Surface((width, height))
        total_text_surface.fill(GREEN)
        y_coord = 0
        for text_surface in text_surfaces :
            total_text_surface.blit(text_surface, (0, y_coord))
            y_coord += text_surface.get_rect().height
        total_text_rect = total_text_surface.get_rect()
        total_text_rect.center = pygame.display.get_surface().get_rect().center
        pygame.display.get_surface().blit(total_text_surface, total_text_rect.topleft)
