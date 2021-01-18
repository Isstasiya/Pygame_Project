import pygame
import os
import sys
import argparse
from random import choice
import sqlite3

# sound_boom = pygame.mixer.Sound('Data/boom.ogg')
# sound_boom.play()
pygame.mixer.pre_init(44100, -16, 1, 512)
geeeeee = 0
pause = True
music = ['1_music.mp3', '2_music.mp3', '3_music.mp3']

maps = ["map.map", "close_zone.map", "free_zone.map"]
parser = argparse.ArgumentParser()
parser.add_argument("map", type=str, nargs="?", default=choice(maps))
args = parser.parse_args()
map_file = args.map

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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

pygame.init()
screen_size = (1200, 800) #screen size
screen = pygame.display.set_mode(screen_size)
FPS = 60

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png'),
    'wall_2': load_image('wall_2.png')#all images
}
player_image = load_image('mar.png')

tile_width = tile_height = 50 #tile size


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 20)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos_star = self.pos
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_width * self.pos[1] - 20)


player = None
running = True
clock = pygame.time.Clock()

sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit


def start_screen(): #shows start screen
    pygame.mixer.music.load('Data/start_window.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, (180, 0, 0), (440, 270, 400, 200), 4)
    pygame.draw.rect(screen, (50, 50, 50), (443, 273, 400 - 4, 200 - 4), 0)

    pygame.font.init()
    myfont_start = pygame.font.Font('Data/20051.ttf', 100)
    textsurface_start = myfont_start.render('Start', False, (200, 200, 200))
    screen.blit(textsurface_start, (510, 300))

    myfont_start_score = pygame.font.Font('Data/19950.otf', 50)
    textsurface_start_score = myfont_start_score.render('Best score:', False, (255, 255, 255))
    screen.blit(textsurface_start_score, (20, 740))

    textsurface_start_score = myfont_start_score.render('00000', False, (255, 255, 255))
    screen.blit(textsurface_start_score, (200, 740))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 440 and event.pos[0] < 440 + 400 and event.pos[1] > 270 and event.pos[1] < 270 + 200:
                    pygame.mixer.music.stop()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "Data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

def pause_def():
    pygame.font.init()
    myfont_pause = pygame.font.SysFont('Comic Sans MS', 100)
    textsurface_pause = myfont_pause.render('Pause', False, (0, 0, 0))
    screen.blit(textsurface_pause, (500, 250))
    global pause
    pause = not pause
    if pause:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '/':
                Tile('wall_2', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            hero.move(x + 1, y)

#show start screen
start_screen()

level_map = load_level(map_file)
hero, max_x, max_y = generate_level(level_map)
#музыка в игре
pygame.mixer.music.load('Data/' + music[0])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(1)
pygame.mixer.music.queue('Data/' + music[1])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(1)
pygame.mixer.music.queue('Data/' + music[2])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pause:

                pygame.font.init()
                myfont_pause = pygame.font.SysFont('Comic Sans MS', 100)
                textsurface_pause = myfont_pause.render('', False, (0, 0, 0))
                screen.blit(textsurface_pause, (300, 100))

                if event.key == pygame.K_UP:
                    move(hero, "up")
                elif event.key == pygame.K_DOWN:
                    move(hero, "down")
                elif event.key == pygame.K_LEFT:
                    move(hero, "left")
                elif event.key == pygame.K_RIGHT:
                    move(hero, "right")

            if event.key == pygame.K_p:
                pause_def()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 1150 and event.pos[0] < 1192 and event.pos[1] > 755 and event.pos[1] < 755 + 42:
                pause_def()

    if pause:
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)

        hero_group.draw(screen)

        image_player = pygame.image.load('data/mar.png')
        image_player = image_player.convert_alpha()
        screen.blit(image_player, (90, 755))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface_you = myfont.render('You:', False, (255, 255, 255))
        screen.blit(textsurface_you, (10, 750))

        textsurface_bestscore = myfont.render('Best score:', False, (255, 255, 255))
        screen.blit(textsurface_bestscore, (200, 755))

        con = sqlite3.connect('database')
        cur = con.cursor()
        result = cur.execute("""SELECT res FROM results WHERE id_res = 1""").fetchall()
        textsurface_bestscore_n = myfont.render(str(result[0][0]), False, (255, 255, 255))
        screen.blit(textsurface_bestscore_n, (370, 755))
        con.close()

        textsurface_score = myfont.render('Score:', False, (255, 255, 255))
        screen.blit(textsurface_score, (470, 755))

        geeeeee += 1
        textsurface_score_n = myfont.render(str(geeeeee), False, (255, 255, 255))
        screen.blit(textsurface_score_n, (600, 755))

        textsurface_pause = myfont.render('Pause - P(key)', False, (255, 255, 255))
        screen.blit(textsurface_pause, (750, 755))
# draw pause button
        pygame.draw.rect(screen, (255, 255, 255), (1150, 755, 42, 42), 2)
        pygame.draw.rect(screen, (50, 50, 50), (1152, 757, 42 - 3, 42 - 3), 0)
        pygame.draw.rect(screen, (100, 100, 100), (1152 + 9, 757 + 6, 6, 42 - 15), 0)
        pygame.draw.rect(screen, (100, 100, 100), (1152 + 25, 757 + 6, 6, 42 - 15), 0)

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()