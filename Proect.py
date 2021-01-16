import pygame
import os
import sys
import argparse
from random import choice

geeeeee = '0'
pause = True

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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
    return new_player, x, y

pygame.init()
screen_size = (1900, 1000) #screen size
screen = pygame.display.set_mode(screen_size)
FPS = 60

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png') #all images
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
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos_star = self.pos
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_width * self.pos[1] + 5)


player = None
running = True
clock = pygame.time.Clock()

sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit


def start_screen(): #shows start screen
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, (180, 0, 0), (730, 400, 400, 200), 4)
    pygame.draw.rect(screen, (50, 50, 50), (733, 403, 400 - 4, 200 - 4), 0)

    pygame.font.init()
    myfont_start = pygame.font.Font('Data/20051.ttf', 100)
    textsurface_start = myfont_start.render('Start', False, (200, 200, 200))
    screen.blit(textsurface_start, (800, 430))

    myfont_start_score = pygame.font.Font('Data/19950.otf', 50)
    textsurface_start_score = myfont_start_score.render('Best score:', False, (255, 255, 255))
    screen.blit(textsurface_start_score, (40, 40))

    textsurface_start_score = myfont_start_score.render('00000', False, (255, 255, 255))
    screen.blit(textsurface_start_score, (220, 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 730 and event.pos[0] < 730 + 400 and event.pos[1] > 400 and event.pos[1] < 400 + 200:
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
    screen.blit(textsurface_pause, (800, 400))
    global pause
    pause = not pause

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pause:

                pygame.font.init()
                myfont_pause = pygame.font.SysFont('Comic Sans MS', 100)
                textsurface_pause = myfont_pause.render('', False, (0, 0, 0))
                screen.blit(textsurface_pause, (800, 400))

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
            if event.pos[0] > 1800 and event.pos[0] < 1842 and event.pos[1] > 955 and event.pos[1] < 955 + 42:
                pause_def()

    if pause:
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)

        hero_group.draw(screen)

        image_player = pygame.image.load('data/mar.png')
        image_player = image_player.convert_alpha()
        screen.blit(image_player, (90, 955))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface_you = myfont.render('You:', False, (255, 255, 255))
        screen.blit(textsurface_you, (10, 955))

        textsurface_bestscore = myfont.render('Best score:', False, (255, 255, 255))
        screen.blit(textsurface_bestscore, (200, 955))

        geeeeee = str(int(geeeeee) + 1)
        textsurface_bestscore_n = myfont.render(geeeeee, False, (255, 255, 255))
        screen.blit(textsurface_bestscore_n, (370, 955))

        textsurface_score = myfont.render('Score:', False, (255, 255, 255))
        screen.blit(textsurface_score, (550, 955))

        textsurface_score_n = myfont.render(geeeeee, False, (255, 255, 255))
        screen.blit(textsurface_score_n, (660, 955))

        textsurface_pause = myfont.render('Pause - P(key)', False, (255, 255, 255))
        screen.blit(textsurface_pause, (800, 955))
# draw pause button
        pygame.draw.rect(screen, (255, 255, 255), (1800, 955, 42, 42), 2)
        pygame.draw.rect(screen, (50, 50, 50), (1802, 957, 42 - 3, 42 - 3), 0)
        pygame.draw.rect(screen, (100, 100, 100), (1802 + 9, 957 + 6, 6, 42 - 15), 0)
        pygame.draw.rect(screen, (100, 100, 100), (1802 + 25, 957 + 6, 6, 42 - 15), 0)


    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()