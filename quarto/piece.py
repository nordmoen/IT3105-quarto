#!/usr/bin/python

class Piece:
    def __init__(self, dark=True, tall=True, square=True, hollow=True):
        self.val = 0
        if dark:
            self.val += 8
        if tall:
            self.val += 4
        if square:
            self.val += 2
        if hollow:
            self.val += 1

    def __eq__(self, other):
        return self.val & other.val > 0 or self.val | other.val < 15 

    def __nq__(self, other):
        return not self == other

    def __str__(self):
        res = '{color}'.format(color='d' if self.val & 8 else 'l')
        if self.val & 4:
            res = res.upper()
        if self.val & 1:
            res += '*'
        if self.val & 2:
            f_brace = '['
            b_brace = ']'
        else:
            f_brace = '('
            b_brace = ')'
        return '{f}{r}{b}'.format(f=f_brace, r=res, b=b_brace)

    def __repr__(self):
        return self.val
