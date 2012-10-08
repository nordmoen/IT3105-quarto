#!/usr/bin/python
from random_player import RandomPlayer

class HumanPlayer(RandomPlayer):
    def get_piece(self, board, pieces):
        '''Function returning the piece to be placed by the opponent,
        can be copied to the other players'''
        if pieces:
            print 'Pieces left: {}'.format(zip(range(16), map(str, pieces)))
            next = raw_input('Select next piece [0, {}]: '.format(len(pieces)-1))
            while 0 > next > len(pieces):
                print 'Selection is out of range'
                next = raw_input('Select next piece [0, {}]: '.format(len(pieces)-1))
            return pieces[int(next)]
        return None

    def get_placement(self, board, piece, pieces):
        print board
        print 'Place the piece: {}'.format(piece)
        x, y = raw_input('X, Y: ').split(',')
        pos = (int(x), int(y))
        return pos
