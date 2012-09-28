#!/usr/bin/python

class Piece:
    def __init__(self, dark=True, tall=True, square=True, hollow=True, val=None):
        if val != None:
            if 0 <= val < 16:
                self.val = val
            else:
                raise ValueError('Value is outside range [0, 15]. Value is {value}'.format(value=val))
        else:                
            self.val = 0
            if dark:
                self.val += 8
            if tall:
                self.val += 4
            if square:
                self.val += 2
            if hollow:
                self.val += 1
        self.xor_val = self.val ^ 15

    def __eq__(self, other):
        try:
            return self.val & other.val > 0 or self.xor_val & other.xor_val > 0
        except AttributeError:
            return False

    def __nq__(self, other):
        return not self == other

    def __str__(self):
        res = '{color}'.format(color='d' if self.val & 8 else 'l')
        if self.val & 4:
            res = res.upper()
        if self.val & 1:
            res += '*'
        else:
            res += ' '
        if self.val & 2:
            f_brace = '['
            b_brace = ']'
        else:
            f_brace = '('
            b_brace = ')'
        return '{f}{r}{b}'.format(f=f_brace, r=res, b=b_brace)

    def __repr__(self):
        return str(self.val)

def check_four(a,b,c,d):
    try:
        return a.val & b.val & c.val & d.val > 0 or a.xor_val & b.xor_val & c.xor_val & d.xor_val > 0
    except AttributeError:
        return False
