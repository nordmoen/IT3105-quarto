#!/usr/bin/python

import threading
from quarto.piece import Piece
from quarto.board import Board

class ServerThread(threading.Thread):
    '''A class which will simulate a game between two players
    in a threaded manner to ensure that we can have several
    playing at the same time'''

    def __init__(self, player1, player2):
        threading.Thread.__init__(self)
        self.p1 = player1
        self.p2 = player2
        self.winner = None

    def run(self):
        self.p1.new_game()
        self.p2.new_game()
        pieces = {i:Piece(val=i) for i in range(16)}
        board = Board()
        placePiece = self.p1.get_piece(board, pieces.values())
        del pieces[placePiece.val]
        nextPlayer = self.p2
        other = self.p1
        victory = None
        while board.size < 16 and not victory:
            placePos = nextPlayer.get_placement(board, placePiece, pieces.values())
            try:
                board.place(placePiece, *placePos)
            except PlaceTakenError:
                self.p1.error()
                self.p2.error()
                return
            other.piece_placed(placePiece, placePos)
            if pieces:
                placePiece = nextPlayer.get_piece(board, pieces.values())
                del pieces[placePiece.val]
            victory = board.check_victory(placePos)
            if nextPlayer == self.p1:
                nextPlayer = self.p2
                other = self.p1
            else:
                nextPlayer = self.p1
                other = self.p2
        if victory:
            if nextPlayer == self.p1:
                self.winner = self.p2
            else:
                self.winner = self.p1


    def get_winner(self):
        return self.winner
