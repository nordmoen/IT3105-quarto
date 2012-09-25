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

    def __cmp__(self, other):
        if other:
            '''Color has most to say. Eg Any dark piece is greater
            than a light piece. If they are the same color then
            tall vs low kick in, where taller is better and so on'''
            if self.color and not other.color:
                return 1
            elif not self.color and other.color:
                return -1
            elif self.tall and not other.tall:
                return 1
            elif not self.tall and other.tall:
                return -1
            elif self.square and not other.square:
                return 1
            elif not self.square and other.square:
                return -1
            elif self.hollow and not other.hollow:
                return 1
            elif not self.hollow and other.hollow:
                return -1
            else:
                return 0
        else:
            return 1
