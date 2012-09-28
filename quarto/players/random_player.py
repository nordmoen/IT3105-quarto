#!/usr/bin/python

from random import choice

class RandomPlayer:
  '''A random Quarto player implementation'''
  def __init__(self):
    self.placePiece = None


  def get_piece(self, pieces):
    '''Function returning the piece to be placed by the opponent,
        can be copied to the other players'''
    if self.placePiece:
      return self.placePiece
    else:
      return choice(pieces)


  def get_placement(self, board, piece, pieces):
    '''Decide where to put #piece on the #board, and which
        piece from the possible #pieces to return to the other player'''
    placed = False
    while not placed:
      x = choice(range(4))
      y = choice(range(4))
      if not board.get(x, y):
        placed = True
    self.placePiece = choice(pieces)
    return (x, y)
