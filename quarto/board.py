#!/usr/bin/python
from piece import check_four

class Board:
    '''A Quarto board implementation'''
    def __init__(self):
        self.board = [[None, None, None, None] for i in range(4)]
        self.placed = 0

    def place(self, piece, x, y):
        if self.board[y][x]:
            raise PlaceTakenError((x, y), str(self))
        else:
            self.board[y][x] = piece
            self.placed += 1

    def get(self, x, y):
        return self.board[y][x] if self.board[y][x] else None

    def check_victory(self, pos):
        start_piece = self.get(*pos)
        if not start_piece:
            return None

        if check_four(*[self.get(i, pos[1]) for i in range(4)]):
            return (1, 0)
        if check_four(*[self.get(pos[0], i) for i in range(4)]):
            return (0, 1)
        if self.__is_cross(pos):
            if check_four(*[self.get(i, i) for i in range(4)]): 
                return (1, 1)
        if self.__is_cross(pos, False):
            if check_four(*[self.get(i, 3-i) for i in range(4)]):
                return (3, -1)
        return None
    
    def __is_cross(self, pos, top = True):
        return pos[0] == pos[1] if top else pos[0] == 3-pos[1]

    def __str__(self):
        return '\n'.join(', '.join(str(piece) if piece else ' '*4 for piece in row) for row in self.board)
    def __repr(self):
        return repr(self.board)


class PlaceTakenError(Exception):
    """Exception raised when a piece is tried to be placed
    on top of another piece"""

    def __init__(self, pos, board=''):
        self.pos = pos
        self.board = board

    def __str__(self):
        return 'A piece is already placed in x: {x_pos}, y: {y_pos}\n{b}'.format(
                x_pos=self.pos[0], y_pos=self.pos[1], b=self.board)
