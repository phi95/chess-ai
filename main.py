"""
Chess-AI
"""
import itertools
import pygame as pg
import chess
pg.init()
pg.font.init()

TITLE = "CHESS - AI"
BLACK_PLAYER = "black"
WHITE_PLAYER = "white"

TILE_SIZE = 60
WIDTH = 8*TILE_SIZE
HEIGHT = 8*TILE_SIZE

RGB_GRAY = (140, 140, 140)
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
RGB_GREEN = (0, 255, 0)

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

colors = itertools.cycle((RGB_WHITE, RGB_GRAY))
background = pg.Surface((WIDTH, HEIGHT))

#background
for y in range(0, HEIGHT, TILE_SIZE):
    for x in range(0, WIDTH, TILE_SIZE):
        rect = (x, y, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(background, next(colors), rect)
    next(colors)

board_pieces = chess.init_pieces(BLACK_PLAYER)
board_pieces.update(chess.init_pieces(WHITE_PLAYER))

def main_loop():

    def draw_screen():
        SCREEN.blit(background, background.get_rect())

        if isHighlight and valids:
            for coord in valids:
                border = (int(coord[0])*TILE_SIZE, int(coord[-1])*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(SCREEN, RGB_BLACK, border)
                pg.draw.rect(SCREEN, RGB_GREEN, (int(coord[0])*TILE_SIZE+1, int(coord[-1])*TILE_SIZE+1, TILE_SIZE-2, TILE_SIZE-2))

        for key in board_pieces:
            SCREEN.blit(board_pieces[key][1], (int(key[0])*TILE_SIZE, int(key[-1])*TILE_SIZE))

        pg.display.update()

    def game_over(winner):
        main_font = pg.font.SysFont("comicsans", 100)
        text_color = RGB_WHITE if winner == WHITE_PLAYER else RGB_BLACK
        background_color = RGB_BLACK if winner == WHITE_PLAYER else RGB_WHITE
        winner_text = main_font.render(f"{winner} wins!", 1, text_color, background_color)
        winner_text_rect = winner_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        while True:
            SCREEN.blit(winner_text, winner_text_rect)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

    isHighlight = False
    valids = []
    current_player_turn = WHITE_PLAYER
    select = None
    winner = None
    while True:
        clock.tick(30)
        draw_screen()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONUP:
                x, y = pg.mouse.get_pos()
                x, y = chess.get_coord(x, y, TILE_SIZE)
                current = f"{x},{y}"

                if not isHighlight:
                    select = current

                    if select in board_pieces and current_player_turn == board_pieces[select][2]:
                        valids = chess.get_valid_moves(board_pieces, select)
                        isHighlight = True
                else:
                    if not valids or current not in valids:
                        valids = []
                    else:
                        if current in board_pieces and board_pieces[current][0] == chess.KING_NAME:
                            winner = board_pieces[select][2]
                        board_pieces[current] = board_pieces[select]
                        del board_pieces[select]
                        select = ""

                        current_player_turn = WHITE_PLAYER if current_player_turn == BLACK_PLAYER else BLACK_PLAYER

                        if winner:
                            isHighlight = False
                            draw_screen()
                            game_over(winner)

                    isHighlight = False


main_loop()