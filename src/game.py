from Scores import Highscores, Score
import instrument
from Text import Text
from Constants import *

class Game :
    def __init__(self, max_round=MAX_ROUND, difficulty=Difficulty.EASY, fretboard_top = None) :
        #Game
        self.won_rounds = 0
        self.timer = 0
        if fretboard_top == None :
            self.fretboard = instrument.FretBoard()
        else :
            self.fretboard = instrument.FretBoard(top = fretboard_top)
        self.round_counter = 0
        self.max_round = max_round
        self.difficulty = difficulty
        self.highscores = Highscores(self.get_supposed_state())
        self.highlighted_score_index = -1

        #Text
        self.text_rule = Text(coordinates=QUESTION_COORDINATES)
        self.text_game_over = Text("Bien joué ! Partie terminée.").center_on_rect(pygame.display.get_surface().get_rect())
        self.game_state = InGameState.PLAY

    def write_score_infos(self) :
        round_writer = Text("Round = "+str(self.round_counter)+"/"+str(self.max_round))
        won_rounds_writer = Text("Score = "+str(self.won_rounds))
        time_writer = Text(self.get_timer_str())
        text_round_surface = round_writer.stick_to_right().stick_to_top().write()
        text_round_bottom = text_round_surface.get_rect().bottom
        text_score = won_rounds_writer.stick_to_right().stick_to_top(text_round_bottom).write()
        text_score_bottom = text_score.get_rect().bottom
        time_writer.stick_to_right().stick_to_top(text_score_bottom).write()

    def get_supposed_state(self) :
        raise NotImplementedError

    def get_timer_str(self) -> str :
        total_seconds = int(self.timer/10)
        str_minutes = str(total_seconds//60)
        str_seconds = str(total_seconds % 60)
        if len(str_seconds) == 1 :
            str_seconds = "0"+str_seconds
        if len(str_minutes) == 1 :
            str_minutes = "0"+str_minutes
        return str_minutes+":"+str_seconds
    
    def manage_event(self, event) :
        match self.game_state :
            case InGameState.PLAY :
                return self.manage_play(event)
            case InGameState.SUCCESS :
                return self.manage_success_failure(event)
            case InGameState.FAILURE :
                return self.manage_success_failure(event)
            case InGameState.GAME_OVER :
                return self.manage_game_over(event)
            
    def manage_play(self, event) :
        if event.type == TENTHSECOND_EVENT :
            self.timer += 1
        elif event.type == pygame.KEYDOWN and event.key == 32 :
            self.fretboard.show_notes = not(self.fretboard.show_notes)
        return self.get_supposed_state()

    def manage_success_failure(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if self.round_counter < self.max_round :
                self.start_round()
                self.game_state = InGameState.PLAY
            else :
                self.enter_game_over()
                self.game_state = InGameState.GAME_OVER
        return self.get_supposed_state()

    def manage_game_over(self, event) :
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            return States.HOME
        else :
            return self.get_supposed_state()
    
    def start_round(self) :
        self.round_counter += 1
        self.game_state = InGameState.PLAY

    def display(self) :
        pygame.display.get_surface().fill(GREEN)
        match self.game_state :
            case InGameState.PLAY :
                self.display_play()
            case InGameState.SUCCESS :
                self.display_success()
            case InGameState.FAILURE :
                self.display_failure()
            case InGameState.GAME_OVER :
                self.display_game_over()
        self.write_score_infos()

    def enter_game_over(self) :
        self.game_state = InGameState.GAME_OVER
        score = Score(self.won_rounds, self.get_timer_total_seconds())
        self.highlighted_score_index = self.highscores.add(score)

    def get_timer_total_seconds(self) -> int :
        return int(self.timer/10)
    
    def handle_correct(self) :
        self.won_rounds += 1
        self.game_state = InGameState.SUCCESS

    def handle_incorrect(self) :
        self.game_state = InGameState.FAILURE

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