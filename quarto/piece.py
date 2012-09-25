#!/usr/bin/python

class Piece:
    def __init__(self, dark=True, tall=True, square=True, hollow=True):
        self.color = dark
        self.tall = tall
        self.square = square
        self.hollow = hollow

    def __eq__(self, other):
        return (self.color == other.color or self.tall == other.tall or
                self.square == other.square or self.hollow == other.hollow)

    def __nq__(self, other):
        return not self == other

    def __str__(self):
        res = '{color}'.format(color='d' if self.color else 'l')
        if self.tall:
            res = res.upper()
        if self.hollow:
            res += '*'
        if self.square:
            f_brace = '['
            b_brace = ']'
        else:
            f_brace = '('
            b_brace = ')'
        return '{f}{r}{b}'.format(f=f_brace, r=res, b=b_brace)

    def __repr__(self):
        return str(self)
