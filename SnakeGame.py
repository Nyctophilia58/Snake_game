import pygame
import sys
import random
from pygame.math import Vector2
import time
import json


class Snake:
    def __init__(self):
        self.head = 0
        self.tail = 0
        self.game_close = False

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Pictures/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Pictures/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Pictures/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Pictures/head_right.png').convert_alpha()

        self.body_tr = pygame.image.load('Pictures/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Pictures/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Pictures/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Pictures/body_bl.png').convert_alpha()

        self.body_vertical = pygame.image.load('Pictures/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Pictures/body_horizontal.png').convert_alpha()

        self.tail_up = pygame.image.load('Pictures/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Pictures/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Pictures/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Pictures/tail_right.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("Crunch.wav")  # wav file

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                dis.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                dis.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    dis.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    dis.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        dis.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        dis.blit(self.body_tr, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        dis.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        dis.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        relation_head = self.body[1] - self.body[0]
        if relation_head == Vector2(1, 0):
            self.head = self.head_left
        elif relation_head == Vector2(-1, 0):
            self.head = self.head_right
        elif relation_head == Vector2(0, 1):
            self.head = self.head_up
        elif relation_head == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        relation_tail = self.body[-2] - self.body[-1]
        if relation_tail == Vector2(1, 0):
            self.tail = self.tail_left
        elif relation_tail == Vector2(-1, 0):
            self.tail = self.tail_right
        elif relation_tail == Vector2(0, 1):
            self.tail = self.tail_up
        elif relation_tail == Vector2(0, -1):
            self.tail = self.tail_down

    def add_block(self):
        self.new_block = True

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def play_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = 0
        self.count = 0
        self.randomize()

    def draw_fruit(self):
        if self.count == 5:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size*100,
                                     cell_size*100)
            self.count = 0
        else:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            self.count += 1
        dis.blit(apple, fruit_rect)
        # pygame.draw.rect(dis, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    score = 0

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.grass_draw()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.score = self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            game_over_page(self.score)

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.reset()

    def grass_draw(self):
        grass_color = (138, 154, 91)
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(dis, grass_color, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(dis, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        value = game_font.render(score_text, False, red)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = value.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 5,
                              apple_rect.height)
        pygame.draw.rect(dis, orange, bg_rect)
        dis.blit(value, score_rect)
        dis.blit(apple, apple_rect)
        return int(score_text)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 30
cell_number = 30

black = (0, 0, 0)
orange = (255, 165, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 102)
purple = (100, 50, 150)

dis_width = cell_size * cell_number
dis_height = cell_size * cell_number
dis = pygame.display.set_mode((dis_width, dis_height))
clock = pygame.time.Clock()

apple = pygame.image.load('Pictures/apple.png').convert_alpha()
game_font = pygame.font.Font(None, 25)  # Default font or you can add ttf file
display_msg_font = pygame.font.Font(None, 60)
menu_font = pygame.font.Font(None, 40)

background = pygame.image.load('Pictures/background.png')
# bg = pygame.image.load('Pictures/bg.png')

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)
main_game = Main()


def button(screen, position, text, size, colors="white"):
    fg = colors
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, True, fg)
    x, y = position
    return screen.blit(text_render, (x, y))


def message(msg, color, place):
    msg = display_msg_font.render(msg, False, color)
    dis.blit(msg, place)


def save_score(name, score):
    with open("score.txt", "a") as f:
        f.write(name + "\t" + str(score) + "\n")
        f.close()


def welcome_page():
    # display()
    pygame.display.set_caption("SNAKE GAME")
    dis.fill(black)
    dis.blit(background, (0, 0))
    message("***WELCOME TO MY SNAKE GAME***", purple, [100, dis_height / 3 - 100])
    b0 = button(dis, (150, dis_height/3), "NEW GAME", 30, "purple")
    b1 = button(dis, (150, dis_height/3+50), "LOAD GAME", 30, "purple")
    b2 = button(dis, (150, dis_height/3+100), "OPTIONS", 30, "purple")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    b0 = button(dis, (150, dis_height / 3), "NEW GAME", 30, "white")
                else:
                    b0 = button(dis, (150, dis_height / 3), "NEW GAME", 30, "purple")

                if b1.collidepoint(pygame.mouse.get_pos()):
                    b1 = button(dis, (150, dis_height / 3 + 50), "LOAD GAME", 30, "white")
                else:
                    b1 = button(dis, (150, dis_height / 3 + 50), "LOAD GAME", 30, "purple")

                if b2.collidepoint(pygame.mouse.get_pos()):
                    b2 = button(dis, (150, dis_height / 3 + 100), "OPTIONS", 30, "white")
                else:
                    b2 = button(dis, (150, dis_height / 3 + 100), "OPTIONS", 30, "purple")

            if event.type == pygame.MOUSEBUTTONUP:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    game_page()
                elif b1.collidepoint(pygame.mouse.get_pos()):
                    click = 2
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    options_page()
                break
        pygame.display.update()


def game_page():
    pygame.display.set_caption("NEW GAME")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # with open("saved_data.txt", "w") as saved_file:
                #     json.dump(Main.draw_score.score_text)
                pygame.quit()
                sys.exit()
            if event.type == screen_update:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_KP_8:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_KP_2:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP_4:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_KP_6:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_p:
                    pause_page()
        dis.fill(white)
        main_game.draw_elements()
        pygame.display.update()
        clock.tick()


def options_page():
    pygame.display.set_caption("OPTIONS")
    dis.blit(background, (0, 0))
    message("***OPTIONS***", purple, [100, dis_height / 3 - 100])
    b0 = button(dis, (150, dis_height / 3), "GAME SPEED", 30, "purple")
    b1 = button(dis, (150, dis_height / 3 + 50), "SOUND", 30, "purple")
    b2 = button(dis, (150, dis_height / 3 + 100), "SCORE", 30, "purple")
    b3 = button(dis, (150, dis_height / 3 + 150), "BACK", 30, "purple")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    b0 = button(dis, (150, dis_height / 3), "GAME SPEED", 30, "white")
                else:
                    b0 = button(dis, (150, dis_height / 3), "GAME SPEED", 30, "purple")

                if b1.collidepoint(pygame.mouse.get_pos()):
                    b1 = button(dis, (150, dis_height / 3 + 50), "SOUND", 30, "white")
                else:
                    b1 = button(dis, (150, dis_height / 3 + 50), "SOUND", 30, "purple")

                if b2.collidepoint(pygame.mouse.get_pos()):
                    b2 = button(dis, (150, dis_height / 3 + 100), "SCORE", 30, "white")
                else:
                    b2 = button(dis, (150, dis_height / 3 + 100), "SCORE", 30, "purple")

                if b3.collidepoint(pygame.mouse.get_pos()):
                    b3 = button(dis, (150, dis_height / 3 + 150), "BACK", 30, "white")
                else:
                    b3 = button(dis, (150, dis_height / 3 + 150), "BACK", 30, "purple")

            if event.type == pygame.MOUSEBUTTONUP:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    click = 1
                elif b1.collidepoint(pygame.mouse.get_pos()):
                    click = 2
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    show_score()
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    welcome_page()
                break
        pygame.display.update()
        clock.tick()


def game_over_page(score):
    pygame.display.set_caption("EXIT")
    dis.blit(background, (0, 0))
    message(f"Your score is {score}.", purple, (0, 0))
    message("Your name: ", purple, (0, 50))
    name = ""
    input_rect = pygame.Rect(240, 50, 200, 40)
    color_active = pygame.Color('chartreuse3')
    color_passive = pygame.Color('azure3')
    color = color_passive
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_passive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:    # if enter is pressed
                        save_score(name, score)
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        pygame.draw.rect(dis, color, input_rect, 2)
        text_surface = display_msg_font.render(name, False, purple)
        dis.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width())
        pygame.display.update()
        clock.tick()


def show_score():
    pygame.display.set_caption("SCORE")
    dis.fill((138, 154, 91))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    welcome_page()
        with open("score.txt", "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            lines = [line.split("\t") for line in lines]
            lines.sort(key=lambda x: x[1], reverse=True)
            for j, line in enumerate(lines):
                message(f"{j + 1}. {line[0]} - {line[1]}", purple, (0, j * 50))

        pygame.display.update()


def pause_page():
    pygame.display.set_caption("PAUSE")
    dis.blit(background, (0, 0))
    message("***PAUSE***", purple, [100, dis_height / 3 - 100])
    b0 = button(dis, (150, dis_height / 3), "RESUME", 30, "purple")
    b1 = button(dis, (150, dis_height / 3 + 50), "OPTIONS", 30, "purple")
    b2 = button(dis, (150, dis_height / 3 + 100), "EXIT", 30, "purple")
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    b0 = button(dis, (150, dis_height / 3), "RESUME", 30, "white")
                else:
                    b0 = button(dis, (150, dis_height / 3), "RESUME", 30, "purple")

                if b1.collidepoint(pygame.mouse.get_pos()):
                    b1 = button(dis, (150, dis_height / 3 + 50), "OPTIONS", 30, "white")
                else:
                    b1 = button(dis, (150, dis_height / 3 + 50), "OPTIONS", 30, "purple")

                if b2.collidepoint(pygame.mouse.get_pos()):
                    b2 = button(dis, (150, dis_height / 3 + 100), "EXIT", 30, "white")
                else:
                    b2 = button(dis, (150, dis_height / 3 + 100), "EXIT", 30, "purple")

            if event.type == pygame.MOUSEBUTTONUP:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    paused = False
                elif b1.collidepoint(pygame.mouse.get_pos()):
                    options_page()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    game_over_page(main_game.score)
                break

        pygame.display.update()
        clock.tick()


welcome_page()
