#!/usr/bin/python

import logging
from quarto.players import minimax_player
from quarto.piece import Piece
from quarto.board import Board

class Player(object):
    def __init__(self, **kwargs):
        if 'depth' in kwargs:
            self.depth = int(kwargs['depth'])
        else:
            self.depth = 4
        if 'switch' in kwargs:
            self.switch = int(kwargs['switch'])
        else:
            self.switch = 6

        logging.basicConfig(level=logging.CRITICAL)
        self.player = minimax_player.MinimaxPlayer(self.depth, self.switch)

    def perform_action(self, board, piece, pieces):
        our_pieces = map(lambda x: Piece(val=x), pieces)
        our_board = Board()
        for i, p in enumerate(board):
            if p:
                our_board.place(Piece(val=p), *self.__translate_int_pos(i))
        if piece == -1:
            return (self.player.get_piece(our_board, our_pieces).val, -1)
        else:
            pos = self.player.get_placement(our_board, Piece(val=piece), our_pieces)
            next_piece = self.player.get_piece(our_board, our_pieces)
            return (next_piece.val, self.__translate_pos_int(pos))

    def __translate_pos_int(self, pos):
        return pos[1]*4 + pos[0]

    def __translate_int_pos(self, i):
        x = i % 4
        y = (i - x) / 4
        return (x, y)

    def __str__(self):
        return 'T&J ' + str(self.player)
