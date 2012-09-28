#!/usr/bin/python

class Board:
    '''A Quarto board implementation'''
    def __init__(self):
        self.board = [[16, 16, 16, 16] for i in range(4)]

    def place(self, piece, x, y):
        if self.board[y][x] != 16:
            raise PlaceTakenError((x, y), str(self))
        else:
            self.board[y][x] = piece

    def get(self, x, y):
        return self.board[y][x] if self.board[y][x] != 16 else None

    def check_victory(self, pos):
        start_piece = self.get(*pos)
        if not start_piece:
            return None
        row = [self.get(pos[0], i) for i in range(4)] #not done here
        if self.__is_cross(pos):
            if all(in_a_cross):
                return (1, 1)
        if self.__is_cross(pos, False):
            if all(in_a_cross2):
                return (3, -1)
        return None
    
    def __is_cross(self, pos, top = True):
        return pos[0] == pos[1] if top else pos[0] == 3-pos[1]

    def __str__(self):
        return '\n'.join(', '.join(str(piece) if piece != 16 else ' ' for piece in row) for row in self.board)
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
