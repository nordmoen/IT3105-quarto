#!/usr/bin/python

import threading
from quarto import game

class ServerThread(threading.Thread):
    '''A class which will simulate a game between two players
    in a threaded manner to ensure that we can have several
    playing at the same time'''

    def __init__(self, player1, player2):
        threading.Thread.__init__(self)
        self.player1 = player1
        self.player2 = player2

    def run(self):
       game = game.Game(self.player1, self.player2)
       self.stats = game.play()

    def get_stats(self):
        return self.stats
