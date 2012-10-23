#!/usr/bin/python

import threading
from quarto.piece import Piece
from quarto.board import Board, PlaceTakenError

class ServerThread(threading.Thread):
    '''A class which will simulate a game between two players
    in a threaded manner to ensure that we can have several
    playing at the same time'''

    def __init__(self, player1, player2):
        threading.Thread.__init__(self)
        self.p1 = player1
        self.p2 = player2
        self.winner = None
        self.board = None
        self.ex = None

    def run(self):
        pieces = {i:Piece(val=i) for i in range(16)}
        board = Board()
        placePiece = self.p1.get_piece(board, pieces.values())
        del pieces[placePiece.val]
        nextPlayer = self.p2
        other = self.p1
        victory = None
        try:
            while board.placed < 16 and not victory:
                placePos = nextPlayer.get_placement(board, placePiece, pieces.values())
                board.place(placePiece, *placePos)
                nextPlayer.piece_placed(placePiece, placePos)
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
            self.board = board
            if victory:
                if nextPlayer == self.p1:
                    self.winner = self.p2
                else:
                    self.winner = self.p1
        except Exception, e:
            self.winner = None
            self.board = None
            self.ex = e

    def get_last_exception(self):
        return self.ex

    def get_winner(self):
        return self.winner, self.board
