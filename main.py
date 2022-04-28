from logics import *
import random
import pygame
import sys

pygame.init()


mas = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]


BLOCK_COLOR = {
    0: (205, 194, 181),
    2: (238, 229, 219),
    4: (237, 225, 201),
    8: (238, 179, 121),
    16: (239, 149, 97),
    32: (239, 124, 92),
    64: (239, 92, 50),
    128: (235, 208, 116),
    256: (235, 208, 116),
    512: (235, 201, 80),
    1024: (235, 201, 80),
    2048: (234, 196, 3)
}

TEXT_COLOR = {
    2: (119, 110, 101),
    8: (249, 246, 242)
}

BLOCK = 4
SIZEBLOCK = 110
MARGIN = 10
WIDTH = BLOCK*SIZEBLOCK + 5*MARGIN
HEIGHT = WIDTH+110

score = 0
best_record = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game 2048")
Title = pygame.Rect(0, 0, WIDTH, 110)


class Button:

    def __init__(self, w, h, passive_color, active_color):
        self.w = w
        self.h = h
        self.active_color = active_color
        self.passive_color = passive_color
        self.click = False

    def draw(self, x, y, text, text_color, size, action, *args):
        # flag = True
        font = pygame.font.SysFont('stxingkai', size)

        # while flag:
        click = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        game_rec = pygame.Rect(x, y, self.w, self.h)
        pygame.draw.rect(screen, self.active_color, game_rec)

        game = font.render(text, True, text_color)
        game_w, game_h = game.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if x < pos[0] < self.w+x and y < pos[1] < self.h+y:
            pygame.draw.rect(screen, self.active_color, game_rec)
            screen.blit(game, (((x+(x+self.w))/2)-game_w /
                               2, ((y+(y+self.h))/2)-game_h/2))
            if click[0]:
                print('нажата')
                # flag = False
                func = globals()[action]
                func(*args)
                # self.click = True

        else:
            pygame.draw.rect(screen, self.passive_color, game_rec)
            screen.blit(game, (((x+(x+self.w))/2)-game_w /
                               2, ((y+(y+self.h))/2)-game_h/2))

        pygame.display.update()


def draw_inter(mas, best_record, score):

    screen.fill((187, 175, 161))
    pygame.draw.rect(screen, (250, 248, 239), Title)

    font_score = pygame.font.SysFont('stxingkai', 40)
    text_score = font_score.render('SCORE', True, (236, 214, 171))
    text_score_value = font_score.render(f"{score}", True, (210, 201, 182))
    score_w, score_h = text_score.get_size()
    # score_rec = pygame.Rect(70, 10, score_w+20, score_h+60)

    # pygame.draw.rect(screen, (187, 175, 161), score_rec)
    screen.blit(text_score, (80, 20))
    screen.blit(text_score_value, (80, 30+score_h))

    font_best = pygame.font.SysFont('stxingkai', 40)
    text_best = font_score.render('BEST', True, (236, 214, 171))
    text_best_value = font_best.render(f"{best_record}", True, (210, 201, 182))
    best_w, best_h = text_best.get_size()
    # best_rec = pygame.Rect(300, 10, best_w+50, best_h+60)

    # pygame.draw.rect(screen, (187, 175, 161), best_rec)
    screen.blit(text_best, (325, 20))
    screen.blit(text_best_value, (325, 30+best_h))

    font = pygame.font.SysFont('stxingkai', 100)

    for row in range(4):
        for column in range(4):
            value = mas[row][column]
            if value < 8:
                text = font.render(f"{value}", True, TEXT_COLOR[2])
            else:
                text = font.render(f"{value}", True, TEXT_COLOR[8])

            w = column * SIZEBLOCK + (column + 1) * MARGIN
            h = row * SIZEBLOCK + (row + 1) * MARGIN + SIZEBLOCK
            pygame.draw.rect(
                screen, BLOCK_COLOR[value], (w, h, SIZEBLOCK, SIZEBLOCK))

            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZEBLOCK - font_w) / 2
                text_y = h + (SIZEBLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


def draw_gameover():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((255, 255, 255))
    surf.set_alpha(170)
    screen.blit(surf, (0, 0))

    font = pygame.font.SysFont('stxingkai', 100)
    text_gameover = font.render('Game over!', True, (119, 110, 101))
    screen.blit(text_gameover, (50, 135))

    button_tryagain = Button(150, 38, (142, 123, 103), (166, 145, 121))
    button_backmenu = Button(150, 38, (142, 123, 103), (166, 145, 121))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        button_tryagain.draw((WIDTH/2+5)/2-55.5, 250,
                             'try again', (244, 239, 233), 40, 'start_game')
        button_backmenu.draw((WIDTH/2+5)/2+146.5, 250,
                             'menu', (244, 239, 233), 40, 'draw_menu')

        pygame.display.update()


def start_game():
    global mas, best_record, delta, score

    list_zero = get_empty_list(mas)
    rendom_coords = random.choice(list_zero)
    list_zero.remove(rendom_coords)
    mas = insert_2or4(mas, rendom_coords)

    while True:
        delta = 0
        is_mas_move = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                score += delta

                if score > best_record:
                    best_record = score

                if is_zero_in_mas(mas) and is_mas_move:
                    list_zero = get_empty_list(mas)
                    rendom_coords = random.choice(list_zero)
                    list_zero.remove(rendom_coords)
                    mas = insert_2or4(mas, rendom_coords)
                    is_mas_move = False

        if not can_move(mas) and not is_zero_in_mas(mas):
            print("THE END")
            mas = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
            score = 0
            draw_gameover()

        draw_inter(mas, best_record, score)
        pygame.display.update()


def settings():
    print('soon')


def exit():
    print('выход')
    sys.exit()


def draw_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 229, 204))

    # font = pygame.font.SysFont('stxingkai', 100)

    button_play = Button(200, 98, (255, 229, 204), (245, 219, 201))
    button_settings = Button(300, 98, (255, 229, 204), (245, 219, 201))
    button_exit = Button(400, 98, (255, 229, 204), (245, 219, 201))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        button_play.draw(WIDTH/2-200/2, 68, 'PLAY',
                         (255, 255, 255), 100, 'start_game')
        button_settings.draw(WIDTH/2-300/2, 204, 'settings',
                             (255, 255, 255), 100, 'settings')
        button_exit.draw(WIDTH/2-400/2, 340, 'exit',
                         (255, 255, 255), 100, 'exit')

        pygame.display.update()


if __name__ == "__main__":
    draw_menu()

# pygame.quit()
# quit()
