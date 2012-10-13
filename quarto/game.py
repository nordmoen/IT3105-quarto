#!/usr/bin/python

from board import Board, PlaceTakenError
from piece import Piece

class Game:
    '''A game master for keeping track of games of Quarto'''
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play(self):
        board = Board()
        pieces = {i:Piece(val=i) for i in range(16)}
        placePiece = self.p1.get_piece(board, pieces.values())
        del pieces[placePiece.val]
        nextPlayer = self.p2
        victory = None
        while not victory and board.placed != 16:
            placePos = nextPlayer.get_placement(board, placePiece, pieces.values())
            try:
                board.place(placePiece, *placePos)
            except PlaceTakenError:
                raise PlaceTakenError(placePos, '1' if nextPlayer==self.p1 else
                        '2', board)
            if pieces:
                placePiece = nextPlayer.get_piece(board, pieces.values())
                del pieces[placePiece.val]
            victory = board.check_victory(placePos)
            if nextPlayer == self.p1:
                nextPlayer = self.p2
            else:
                nextPlayer = self.p1
        if not victory:
            winningPlayer = None
        elif nextPlayer == self.p1:
          winningPlayer = self.p2
        else:
          winningPlayer = self.p1
        return (winningPlayer, board, victory, placePos)
