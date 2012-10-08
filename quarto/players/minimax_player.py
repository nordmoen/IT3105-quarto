#!/usr/bin/python

from random import choice
from novice_player import NovicePlayer
from ..piece import Piece
from cquarto import minimax

class MinimaxPlayer(NovicePlayer):
    def __init__(self, plys, change):
        '''Initiate the minimax player with a configurable amount
        of plies to go down in the recursion and a number of how
        many placements should be with the novice strategy'''
        if(0 < plys <= 15):
            self.plys = plys
        else:
            raise ValueError('Plies need to be between (0, 15]. Ply was {p}'.format(p=plys))
        if(0 <= change <= 15):
            self.change = change
        else:
            raise ValueError('The change position was out of range. Legal range [0, 15], was {}'.format(change))
        self.placePiece = None
    
    def get_piece(self, board, pieces):
        '''Function returning the piece to be placed by the opponent,
        can be copied to the other players'''
        if self.change > 0:
            #return super(MinimaxPlayer, self).get_piece(board, pieces)
            return NovicePlayer.get_piece(self, board, pieces)
        if self.placePiece:
            return self.placePiece
        else:
            return choice(pieces)

    def get_placement(self, board, piece, pieces):
        if self.change > 0:
            self.change -= 2
            #return super(MinimaxPlayer, self).get_placement(board, piece, pieces)
            return NovicePlayer.get_placement(self, board, piece, pieces)
        else:
            pos, next = minimax(piece.val, board.get_board(), self.plys)
            self.placePiece = Piece(val=next) if 0 <= next < 16 else None
            return pos
