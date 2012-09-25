#!/usr/bin/python

class Board:
    '''A Quarto board implementation'''
    def __init__(self):
        self.board = [[None, None, None, None] for i in range(4)]

    def place(self, piece, x, y):
        if self.board[y][x]:
            raise PlaceTakenError((x, y), str(self))
        else:
            self.board[y][x] = piece

    def get(self, x, y):
        return self.board[y][x]

    def check_victory(self, pos):
        start_piece = self.get(*pos)
        if not start_piece:
            return None
        in_a_row = [False]*4
        in_a_col = [False]*4
        in_a_cross = [False]*4
        in_a_cross2 = [False]*4
        for i in range(4):
            in_a_col[i] = self.get(pos[0], i) == start_piece if self.get(pos[0], i) else False
            in_a_row[i] = self.get(i, pos[1]) == start_piece if self.get(i, pos[1]) else False
            in_a_cross[i] = self.get(i, i) == start_piece if self.get(i, i) else False
            in_a_cross2[i] = self.get(i, 3-i) == start_piece if self.get(i, 3-i) else False
        if all(in_a_row):
            return (1, 0)
        if all(in_a_col):
            return (0, 1)
        if self.__is_cross(pos):
            if all(in_a_cross):
                return (1, 1)
        if self.__is_cross(pos, False):
            if all(in_a_cross2):
                return (3, -1)
        return None
    
    def __is_cross(self, pos, top_down=True):
        for i in range(4):
            if pos[0] == i and pos[1] == (i if top_down else 3-i):
                return True
        return False

    def __str__(self):
        return '\n'.join(str(row) for row in self.board)
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
