import pygame
import random
import time
from constants import *


class Game:
    """Main game class for the Sequence Memory game."""

    def __init__(self, window, font, button_font, feedback_font, card_font):
        """Initialize the game with default values."""
        self.window = window
        self.font = font
        self.button_font = button_font
        self.feedback_font = feedback_font
        self.card_font = card_font
        self.sequence = []
        self.shuffled_sequence = []
        self.player_sequence = []
        self.state = STATE_INIT
        self.show_time = 0
        self.wrong_message = ""
        self.wrong_time = 0
        self.current_card_index = 0
        self.is_flipping_back = False
        self.flip_back_time = 0

        self.card_back = pygame.image.load("card_image.jpg")
        self.card_back = pygame.transform.scale(
            self.card_back, (CARD_SIZE, CARD_SIZE))

        self.generate_sequence()

    def generate_sequence(self) -> None:
        """Generate a new random sequence and reset game state."""
        self.sequence = [random.randint(0, 9) for _ in range(SEQUENCE_LENGTH)]
        self.shuffled_sequence = self.sequence.copy()
        random.shuffle(self.shuffled_sequence)
        self.player_sequence = []
        self.state = STATE_INIT
        self.show_time = time.time() + INIT_TIME
        self.wrong_message = ""
        self.current_card_index = 0
        self.is_flipping_back = False

    def draw_sequence(self) -> None:
        """Draw the current game state on the screen."""
        self.window.fill(BACKGROUND_COLOR)

        if self.state == STATE_SUCCESS:
            success_text = self.feedback_font.render(
                SUCCESS_TEXT, True, FEEDBACK_FONT_COLOR)
            success_rect = success_text.get_rect(
                center=(CENTER_X, SUCCESS_TEXT_Y))
            self.window.blit(success_text, success_rect)

            self._draw_cards(self.sequence, SEQUENCE_Y, show_all=True)
            self._draw_restart_button()
            return

        current_sequence = {
            STATE_FIRST_SEQUENCE: self.sequence,
            STATE_SECOND_SEQUENCE: self.shuffled_sequence,
            STATE_GUESS: self.sequence,
            STATE_INIT: self.sequence,
            STATE_BREAK: self.shuffled_sequence
        }.get(self.state, self.player_sequence)

        if self.state == STATE_GUESS:

            self._draw_cards(current_sequence, SEQUENCE_Y, show_all=False)

            self._draw_guesses(self.player_sequence,
                               SEQUENCE_Y - CARD_SIZE - 10)
        else:
            show_all = (
                self.state == STATE_FIRST_SEQUENCE and self.current_card_index >= SEQUENCE_LENGTH)
            self._draw_cards(current_sequence, SEQUENCE_Y, show_all=show_all)

        instruction = {
            STATE_INIT: INIT_TEXT,
            STATE_FIRST_SEQUENCE: FIRST_TEXT,
            STATE_BREAK: SECOND_TEXT,
            STATE_SECOND_SEQUENCE: SECOND_TEXT,
            STATE_GUESS: GUESS_TEXT
        }.get(self.state, GUESS_TEXT)

        instruction_text = self.font.render(
            instruction, True, INSTRUCTION_FONT_COLOR)
        instruction_rect = instruction_text.get_rect(
            center=(CENTER_X, INSTRUCTION_TEXT_Y))
        self.window.blit(instruction_text, instruction_rect)

        if self.wrong_message:
            wrong_text = self.feedback_font.render(
                self.wrong_message, True, FEEDBACK_FONT_COLOR)
            wrong_rect = wrong_text.get_rect(
                center=(CENTER_X, FEEDBACK_TEXT_Y))
            self.window.blit(wrong_text, wrong_rect)

        if self.state == STATE_GUESS:
            self._draw_restart_button()

    def _draw_cards(self, sequence, y, show_all=False):
        total_width = (CARD_SIZE * SEQUENCE_LENGTH) + \
            (MARGIN * (SEQUENCE_LENGTH - 1))
        start_x = CENTER_X - total_width // 2

        for i, number in enumerate(sequence):
            x = start_x + (i * (CARD_SIZE + MARGIN))

            self.window.blit(self.card_back, (x, y))

            should_show = (
                show_all or
                (self.state == STATE_FIRST_SEQUENCE and i <= self.current_card_index) or
                (self.state == STATE_SECOND_SEQUENCE and i <= self.current_card_index)
            ) and self.state not in [STATE_INIT, STATE_BREAK]

            if should_show:
                pygame.draw.rect(self.window, CARD_BG_COLOR,
                                 (x, y, CARD_SIZE, CARD_SIZE))
                number_text = self.card_font.render(
                    str(number), True, CARD_FONT_COLOR)
                number_rect = number_text.get_rect(
                    center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
                self.window.blit(number_text, number_rect)

    def _draw_guesses(self, sequence, y):
        """Draw the player's guesses above the cards."""
        total_width = (CARD_SIZE * SEQUENCE_LENGTH) + \
            (MARGIN * (SEQUENCE_LENGTH - 1))
        start_x = CENTER_X - total_width // 2

        for i, number in enumerate(sequence):
            x = start_x + (i * (CARD_SIZE + MARGIN))

            guess_text = self.font.render(str(number), True, CARD_FONT_COLOR)
            guess_rect = guess_text.get_rect(
                center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
            self.window.blit(guess_text, guess_rect)

    def _draw_empty_slot(self, sequence, y):
        total_width = (CARD_SIZE * SEQUENCE_LENGTH) + \
            (MARGIN * (SEQUENCE_LENGTH - 1))
        start_x = CENTER_X - total_width // 2

        for i in range(SEQUENCE_LENGTH):
            x = start_x + (i * (CARD_SIZE + MARGIN))
            self.window.blit(self.card_back, (x, y))

    def _draw_restart_button(self):
        button_rect = pygame.Rect(
            BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.window, BUTTON_BG_COLOR, button_rect)
        restart_text = self.button_font.render(
            BUTTON_TEXT, True, BUTTON_FONT_COLOR)
        restart_rect = restart_text.get_rect(center=button_rect.center)
        self.window.blit(restart_text, restart_rect)
        return button_rect

    def is_restart_clicked(self, pos):
        button_rect = pygame.Rect(
            BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        return button_rect.collidepoint(pos)

    def check_sequence(self) -> bool:
        """Check if the player's sequence matches the original sequence."""
        return self.player_sequence == self.sequence
