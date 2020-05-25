"""
module for pieces
"""
import os
import pygame as pg
pg.init()

ROOK_NAME = "ROOK"
KNIGHT_NAME = "KNIGHT"
BISHOP_NAME = "BISHOP"
QUEEN_NAME = "QUEEN"
KING_NAME = "KING"
PAWN_NAME = "PAWN"

def init_pieces(player):
    bishop_img = pg.image.load(os.path.join("assets", f"{player}_bishop.png"))
    king_img = pg.image.load(os.path.join("assets", f"{player}_king.png"))
    knight_img = pg.image.load(os.path.join("assets", f"{player}_knight.png"))
    pawn_img = pg.image.load(os.path.join("assets", f"{player}_pawn.png"))
    queen_img = pg.image.load(os.path.join("assets", f"{player}_queen.png"))
    rook_img = pg.image.load(os.path.join("assets", f"{player}_rook.png"))

    if player == "black":
        board = {"0,0":(ROOK_NAME, rook_img, player),
                 "1,0":(KNIGHT_NAME, knight_img, player),
                 "2,0":(BISHOP_NAME, bishop_img, player),
                 "3,0":(QUEEN_NAME, queen_img, player),
                 "4,0":(KING_NAME, king_img, player),
                 "5,0":(BISHOP_NAME, bishop_img, player),
                 "6,0":(KNIGHT_NAME, knight_img, player),
                 "7,0":(ROOK_NAME, rook_img, player),
                 "0,1":(PAWN_NAME, pawn_img, player, False),
                 "1,1":(PAWN_NAME, pawn_img, player, False),
                 "2,1":(PAWN_NAME, pawn_img, player, False),
                 "3,1":(PAWN_NAME, pawn_img, player, False),
                 "4,1":(PAWN_NAME, pawn_img, player, False),
                 "5,1":(PAWN_NAME, pawn_img, player, False),
                 "6,1":(PAWN_NAME, pawn_img, player, False),
                 "7,1":(PAWN_NAME, pawn_img, player, False)}
    else:
        board = {"0,7":(ROOK_NAME, rook_img, player),
                 "1,7":(KNIGHT_NAME, knight_img, player),
                 "2,7":(BISHOP_NAME, bishop_img, player),
                 "3,7":(QUEEN_NAME, queen_img, player),
                 "4,7":(KING_NAME, king_img, player),
                 "5,7":(BISHOP_NAME, bishop_img, player),
                 "6,7":(KNIGHT_NAME, knight_img, player),
                 "7,7":(ROOK_NAME, rook_img, player),
                 "0,6":(PAWN_NAME, pawn_img, player, False),
                 "1,6":(PAWN_NAME, pawn_img, player, False),
                 "2,6":(PAWN_NAME, pawn_img, player, False),
                 "3,6":(PAWN_NAME, pawn_img, player, False),
                 "4,6":(PAWN_NAME, pawn_img, player, False),
                 "5,6":(PAWN_NAME, pawn_img, player, False),
                 "6,6":(PAWN_NAME, pawn_img, player, False),
                 "7,6":(PAWN_NAME, pawn_img, player, False)}
    return board

def get_coord(x, y, tile_size):
    return (x//tile_size, y//tile_size)

def check_bounds(x, y):
    if x < 0 or x > 7:
        return False
    if y < 0 or y > 7:
        return False
    return True

def get_valid_moves(board, coord):
    def switch_moves(piece):
        switcher = {
            ROOK_NAME: get_valid_rook_moves(board, coord),
            KNIGHT_NAME: get_knight_moves(board, coord),
            BISHOP_NAME: get_valid_bishop_moves(board, coord),
            QUEEN_NAME: get_valid_queen_moves(board, coord),
            KING_NAME: get_valid_king_moves(board, coord),
            PAWN_NAME: get_valid_pawn_moves(board, coord)
        }
        return switcher.get(piece, [])

    return switch_moves(board[coord][0])

def get_single_move(board, coord, x_move, y_move):
    valids = []
    temp_x = int(coord[0]) + x_move
    temp_y = int(coord[-1]) + y_move

    temp_coord = f"{temp_x},{temp_y}"

    if check_bounds(temp_x, temp_y):
        if ((temp_coord not in board) or
                (temp_coord in board and board[temp_coord][2] != board[coord][2])):
            valids.append(temp_coord)

    return valids


def get_multi_moves(board, coord, x_move, y_move):
    valids = []
    temp_x = int(coord[0]) + x_move
    temp_y = int(coord[-1]) + y_move

    temp_coord = f"{temp_x},{temp_y}"
    opponent_checked = False
    while ((check_bounds(temp_x, temp_y) and
            ((temp_coord not in board) or
             (temp_coord in board and board[temp_coord][2] != board[coord][2]
              and not opponent_checked)))):

        if temp_coord in board and board[temp_coord][2] != board[coord][2]:
            opponent_checked = True

        valids.append(temp_coord)
        temp_x += x_move
        temp_y += y_move
        temp_coord = f"{temp_x},{temp_y}"

    return valids

def get_valid_pawn_moves(board, coord):
    move = -1 if board[coord][2] == "white" else 1
    x = int(coord[0])
    y = int(coord[-1])
    valids = []

    temp_y = y + move

    curr_coord = f"{x},{temp_y}"
    if check_bounds(x, temp_y) and curr_coord not in board:
        valids.append(curr_coord)
        curr_coord = f"{x},{temp_y+move}"
        if curr_coord not in board and not board[coord][3]:
            board[coord] = board[coord][:3] + (True,)
            valids.append(curr_coord)

    curr_coord = f"{x+1},{temp_y}"
    if (check_bounds(x+1, temp_y) and
            curr_coord in board and board[curr_coord][2] != board[coord][2]):
        valids.append(curr_coord)

    curr_coord = f"{x-1},{temp_y}"
    if (check_bounds(x-1, temp_y) and
            curr_coord in board and board[curr_coord][2] != board[coord][2]):
        valids.append(curr_coord)

    return valids

def get_valid_rook_moves(board, coord):
    return (get_multi_moves(board, coord, 1, 0) +
            get_multi_moves(board, coord, -1, 0) +
            get_multi_moves(board, coord, 0, 1) +
            get_multi_moves(board, coord, 0, -1))

def get_valid_bishop_moves(board, coord):
    return (get_multi_moves(board, coord, 1, 1) +
            get_multi_moves(board, coord, -1, 1) +
            get_multi_moves(board, coord, 1, -1) +
            get_multi_moves(board, coord, -1, -1))

def get_valid_queen_moves(board, coord):
    return (get_valid_rook_moves(board, coord) +
            get_valid_bishop_moves(board, coord))

def get_valid_king_moves(board, coord):
    return (get_single_move(board, coord, 1, 0) +
            get_single_move(board, coord, -1, 0) +
            get_single_move(board, coord, 0, 1) +
            get_single_move(board, coord, 0, -1) +
            get_single_move(board, coord, 1, 1) +
            get_single_move(board, coord, -1, 1) +
            get_single_move(board, coord, 1, -1) +
            get_single_move(board, coord, -1, -1))

def get_knight_moves(board, coord):
    return (get_single_move(board, coord, 2, 1) +
            get_single_move(board, coord, 2, -1) +
            get_single_move(board, coord, -2, 1) +
            get_single_move(board, coord, -2, -1) +
            get_single_move(board, coord, 1, 2) +
            get_single_move(board, coord, -1, 2) +
            get_single_move(board, coord, 1, -2) +
            get_single_move(board, coord, -1, -2))
