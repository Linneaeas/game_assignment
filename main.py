import pygame
import time
from constants import *
from game import Game

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sequence Memory")

font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
feedback_font = pygame.font.Font(None, FEEDBACK_FONT_SIZE)
card_font = pygame.font.Font(None, CARD_FONT_SIZE)

game = Game(window, font, button_font, feedback_font, card_font)

running = True
while running:
    current_time = time.time()

    if game.state == STATE_INIT:
        if current_time - game.show_time > INIT_TIME:
            game.state = STATE_FIRST_SEQUENCE
            game.show_time = current_time
    elif game.state == STATE_FIRST_SEQUENCE:
        if current_time - game.show_time > CARD_SHOW_TIME and game.current_card_index < SEQUENCE_LENGTH:
            game.current_card_index += 1
            game.show_time = current_time
        elif game.current_card_index >= SEQUENCE_LENGTH and current_time - game.show_time > SEQUENCE_SHOW_TIME:
            game.state = STATE_BREAK
            game.show_time = current_time
    elif game.state == STATE_BREAK:
        if current_time - game.show_time > BREAK_TIME:
            game.state = STATE_SECOND_SEQUENCE
            game.show_time = current_time
            game.current_card_index = 0
    elif game.state == STATE_SECOND_SEQUENCE:
        if current_time - game.show_time > CARD_SHOW_TIME and game.current_card_index < SEQUENCE_LENGTH:
            game.current_card_index += 1
            game.show_time = current_time
        elif game.current_card_index >= SEQUENCE_LENGTH:
            game.state = STATE_GUESS
            game.current_card_index = 0

    if game.wrong_message and current_time - game.wrong_time > WRONG_TEXT_DURATION:
        game.wrong_message = ""
        game.player_sequence = []

    game.draw_sequence()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.is_restart_clicked(event.pos):
                game.generate_sequence()
        elif event.type == pygame.KEYDOWN and game.state == STATE_GUESS:
            if event.unicode.isdigit() and len(game.player_sequence) < SEQUENCE_LENGTH:
                number = int(event.unicode)
                game.player_sequence.append(number)
                if len(game.player_sequence) == SEQUENCE_LENGTH:
                    if game.check_sequence():
                        game.state = STATE_SUCCESS
                    else:
                        game.wrong_message = WRONG_TEXT
                        game.wrong_time = current_time

    pygame.display.update()

pygame.quit()
