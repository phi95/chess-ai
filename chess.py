import itertools
import pygame as pg
pg.init()

TILE_SIZE = 100
WIDTH = 8*TILE_SIZE
HEIGHT = 8*TILE_SIZE

GRAY = (140, 140, 140)
WHITE = (255, 255, 255)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("CHESS - AI")
clock = pg.time.Clock()

colors = itertools.cycle((WHITE, GRAY))
background = pg.Surface((WIDTH, HEIGHT))

for y in range(0, HEIGHT, TILE_SIZE):
    for x in range(0, WIDTH, TILE_SIZE):
        rect = (x, y, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(background, next(colors), rect)
    next(colors)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()

    screen.blit(background, background.get_rect())

    pg.display.flip()
    clock.tick(30)
