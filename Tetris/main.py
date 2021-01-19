import pygame
from copy import deepcopy
from random import choice, randrange
import os
import sys

pause = True
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000



main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

def load_image(name, color_key=None):
    fullname = os.path.join('Data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

def start_screen(): #shows start screen
    pygame.mixer.music.load('Data/start_window.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    fon = pygame.transform.scale(load_image('fon.jpg'), (RES))
    sc.blit(fon, (0, 0))
    pygame.draw.rect(sc, (180, 0, 0), (200, 370, 400, 200), 4)
    pygame.draw.rect(sc, (50, 50, 50), (203, 373, 400 - 4, 200 - 4), 0)

    pygame.font.init()
    myfont_start = pygame.font.Font('Data/20051.ttf', 100)
    textsurface_start = myfont_start.render('Start', False, (200, 200, 200))
    sc.blit(textsurface_start, (270, 400))

    myfont_start_score = pygame.font.Font('Data/19950.otf', 50)
    textsurface_start_score = myfont_start_score.render('Кибер тетрис', False, (255, 255, 255))
    sc.blit(textsurface_start_score, (300, 20))

    myfont_start_score = pygame.font.Font('Data/19950.otf', 50)
    textsurface_start_score = myfont_start_score.render('Best score:', False, (255, 255, 255))
    sc.blit(textsurface_start_score, (20, 880))

    textsurface_start_score = myfont_start_score.render(str(get_record()), False, (255, 255, 255))
    sc.blit(textsurface_start_score, (200, 880))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 200 and event.pos[0] < 200 + 400 and event.pos[1] > 370 and event.pos[1] < 370 + 200:
                    pygame.mixer.music.stop()
                    return
        pygame.display.flip()
        clock.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit

def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


start_screen()

pygame.mixer.music.load('Data/' + 'pesn.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

bg = pygame.transform.scale(load_image('fon_game.jpg'), (RES))
game_bg = pygame.transform.scale(load_image('fon_1.jpg'), (GAME_RES))

def pause_def():
    pygame.font.init()
    myfont_pause = pygame.font.SysFont('Comic Sans MS', 100)
    textsurface_pause = myfont_pause.render('Pause', False, (250, 250, 0))
    sc.blit(textsurface_pause, (480, 300))
    global pause
    pause = not pause
    if pause:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

while True:
    if pause:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))

        for i in range(lines):
            pygame.time.wait(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_def()
        if pause:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
    if pause:
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break

        center = figure[0]
        figure_old = deepcopy(figure)

        # поворот
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        line, lines = H - 1, 0
        # проверка на линию
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                sound_fall = pygame.mixer.Sound('Data/row.ogg')
                sound_fall.set_volume(0.1)
                sound_fall.play()
                anim_speed += 3
                lines += 1

        score += scores[lines]

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 380
            figure_rect.y = next_figure[i].y * TILE + 185
            pygame.draw.rect(sc, next_color, figure_rect)

        sc.blit(title_tetris, (485, -10))
        sc.blit(title_score, (535, 780))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
        sc.blit(title_record, (525, 650))
        sc.blit(font.render(record, True, pygame.Color('gold')), (550, 710))

        # проигрыш
        for i in range(W):
            if field[0][i]:
                pygame.mixer.music.rewind()
                pygame.mixer.music.pause()
                sound_fall = pygame.mixer.Sound('Data/fall.ogg')
                sound_fall.set_volume(0.1)
                sound_fall.play()
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(100)
                pygame.mixer.music.unpause()
        pygame.display.flip()
        clock.tick(FPS)