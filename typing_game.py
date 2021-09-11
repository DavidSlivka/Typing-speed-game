#!/usr/bin/env python

import pygame
import sys
import time
import random

pygame.init()
pygame.display.set_caption('Type Speed test')

heading_color = (255, 213, 102)
text_color = (240, 240, 240)
result_color = (255, 70, 70)
hint_color = (255, 255, 255)

width = 750
height = 500

screen = pygame.display.set_mode((width, height))


def get_sentence():
    f = open('sentences.txt').read()
    sentences = f.split('\n')
    sentence = random.choice(sentences)
    return sentence


def draw_text(msg, y, font_size, color):
    font = pygame.font.Font(None, font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(width/2, y))
    screen.blit(text, text_rect)
    pygame.display.update()


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.write = False
        self.reset = False
        self.end = False
        self.input_text = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.mistakes = 0
        self.word = get_sentence()

    def reset_game(self):
        pygame.display.update()
        self.reset = False
        self.end = False
        self.input_text = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.mistakes = 0
        self.word = get_sentence()
        if not self.word:
            self.reset_game()
        screen.fill((0, 0, 0))
        draw_text("Typing Speed Test", 80, 80, heading_color)
        pygame.draw.rect(screen, heading_color, (50, 250, 650, 50), 2)
        draw_text(self.word, 200, 28, text_color)
        draw_text("Hint: Click in the rectangle and start typing, hit Enter to show results", 320, 20, hint_color)
        pygame.display.update()

    def show_results(self):
        if not self.end:
            self.total_time = time.time() - self.time_start
            count = 0
            try:
                for i, c in enumerate(self.word):
                    if self.input_text[i] == c:
                        count += 1
            except IndexError:
                pass

            self.end = True
            self.accuracy = abs((count - self.mistakes)) / len(self.word) * 100
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.results = f'Time: {round(self.total_time, 2)} secs Accuracy: {round(self.accuracy)} % Wpm: {round(self.wpm)}'
            draw_text("Reset", self.height - 70, 26, (100, 100, 100))
            pygame.display.update()


if __name__ == '__main__':
    game = Game(width, height)
    clock = pygame.time.Clock()
    game.reset_game()
    run = True
    while run:
        screen.fill((0, 0, 0), (50, 250, 650, 50))
        pygame.draw.rect(screen, heading_color, (50, 250, 650, 50), 2)
        # update the text of user input
        draw_text(game.input_text, 275, 26, (250, 250, 250))

        # Make a red "_" after already typed text
        font = pygame.font.Font(None, 26)
        inp = font.render(game.input_text, True, (250, 250, 250))
        text = font.render('_', True, (255, 0, 0))
        screen.blit(text, (inp.get_width() / 2 + game.width / 2, 270))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                # position of input box
                if 50 <= x <= 650 and 250 <= y <= 300:
                    game.write = True
                    game.input_text = ''
                    game.time_start = time.time()
                # position of reset box
                if 310 <= x <= 510 and y >= 390 and game.end:
                    game.reset_game()

            elif event.type == pygame.KEYDOWN:
                if game.write and not game.end:
                    if event.key == pygame.K_RETURN:
                        game.show_results()
                        draw_text(game.results, 350, 28, result_color)
                        game.end = True

                    elif event.key == pygame.K_BACKSPACE:
                        game.input_text = game.input_text[:-1]

                    else:
                        try:
                            if game.word.startswith(game.input_text + event.unicode):
                                game.input_text += event.unicode
                            else:
                                game.mistakes += 1
                        except:
                            pass

        pygame.display.update()
        clock.tick(60)

