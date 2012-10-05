#!/usr/bin/python
from random import choice
from random_player import RandomPlayer
from ..piece import check_four

class NovicePlayer(RandomPlayer):
    def get_placement(self, board, piece, pieces):
        win, pos = self.has_winning_pos(board, piece)
        if win:
            return pos
        else:
            return super(RandomPlayer, self).get_placement(board, piece, pieces)
    
    def get_piece(self, board, pieces):
        for piece in pieces:
            win, pos = self.has_winning_pos(board, piece)
            if not win:
                return piece
        return choice(pieces)
            
    def has_winning_pos(self, board, piece):
        lewp = range(4)
        for i in lewp:
            row = board.get_row(i)
            col = board.get_column(i)
            for p in lewp:
                if not row[p]:
                    row[p] = piece
                    if check_four(*row):
                        return (True, (p, i))
                if not col[p]:
                    col[p] = piece
                    if check_four(*col):
                        return (True, (i, p))
        diag1 = board.get_diagonal()
        diag2 = board.get_diagonal(False)
        for p in lewp:
            if not diag1[p]:
                diag1[p] = piece
                if check_four(*diag1):
                    return (True, (p, p))
            if not diag2[p]:
                diag2[p] = piece
                if check_four(*diag2):
                    return (True, (p, 3-p))
        return (False, (-1, -1))
