#!/usr/bin/python

import logging
import time

import server_listener
import server_thread
from quarto import game

class Server(object):
    '''The server class which can be used to have multiple quarto games
    running at the same time. The server supports two modes:
        - Game mode, wait for two players to connect and play Quarto
        between them.
        - Server mode, let players connect and disconnect playing players
        against each other in a round-robin fashion.'''

    def __init__(self, addr, port, log = None):
        self.addr = addr
        self.port = port
        if log:
            self.log = log
        else:
            self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Server starting')
        self.players = []
        self.log.debug('Creating server listener')
        self.listener = server_listener.ServerListener(self.players, self.addr,
                self.port)
        self.wins = {}
        self.ties = {}
        self.loses = {}

    def shutdown(self):
        if self.listener:
            self.listener.shutdown()
        for player in self.players:
            player.shutdown()

    def prepare_players(self):
        for player in self.players:
            self.log.debug('Preparing: %s', player)
            self.wins[player] = 0
            self.ties[player] = 0
            self.loses[player] = 0

    def play_game(self, num_rounds=1):
        self.listener.start()
        while len(self.players) < 2:
            self.log.info('Waiting for %i player(s) to connect',
                    2-len(self.players))
            time.sleep(2)
            if not self.listener.is_alive():
                self.log.critical('Server listener died! Shutingdown')
                return
        self.listener.shutdown() #We don't need this any more
        self.log.info('Players connected, starting game')
        self.prepare_players()
        p1 = self.players[0]
        p2 = self.players[1]
        g = game.Game(p1, p2)
        for i in range(num_rounds):
            self.log.debug('Starting round %i', i + 1)
            p1.new_game()
            p2.new_game()
            try:
                winningPlayer, board, victory, placePos = g.play()
                if winningPlayer:
                    self.log.debug('Player %s won the game', winningPlayer)
                    self.log.debug('Board:\n %s', board)
                    self.wins[winningPlayer] += 1
                    loser = p1 if winningPlayer == p2 else p2
                    self.loses[loser] += 1
                else:
                    self.log.debug('Players tied the game')
                    self.log.debug('Board:\n %s', board)
                    self.ties[p1] += 1
                    self.ties[p2] += 1
                g = game.Game(p2, p1)
            except:
                self.log.exception('An error occured while trying to play')
                for p in self.players:
                    p.error()
                return
        self.shutdown()
        self.log.info('Played %i rounds', num_rounds)
        self.log.info('Results:')
        self.log.info('\t Player %s won %i times(%i%), lost %i times(%i%)',
                self.wins[p1], int((float(self.wins[p1])/num_rounds)*100), str(p1),
                self.loses[p1], int((float(self.loses[p1])/num_rounds)*100))
        self.log.info('\t Player %s won %i times(%i%), lost %i times(%i%)', str(p2),
                self.wins[p2], int((float(self.wins[p2])/num_rounds)*100),
                self.loses[p2], int((float(self.loses[p2])/num_rounds)*100))
        self.log.info('\t Ties: %i(%i%)', self.ties[p1],
                int((float(self.ties[p2])/num_rounds)*100))
