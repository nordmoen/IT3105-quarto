#!/usr/bin/python

import logging
import time
import random

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
        if self.listener.listen:
            self.log.info('Shutting down server listener')
            self.listener.shutdown()
        if self.listener.is_alive():
            self.log.warning('Listener thread is stile alive')
        for player in self.players:
            if player.is_alive:
                self.log.info('Shutting down player: %s', player)
                try:
                    player.shutdown(self.wins[player], self.loses[player], self.ties[player])
                except:
                    self.log.exception('Player threw exception while trying to send shutdown')
                    self.log.critical('Stats: %s, %s, %s', self.wins, self.loses, self.ties)

    def prepare_players(self):
        for player in self.players:
            self.prepare_player(player)

    def prepare_player(self, player):
        if player not in self.wins:
            self.log.debug('Preparing: %s', player)
            self.wins[player] = 0
            self.ties[player] = 0
            self.loses[player] = 0

    def play_game(self, num_rounds=1):
        self.log.info('Server starting game mode')
        self.listener.start()
        players_last = len(self.players)
        self.log.info('Waiting for 2 players to connect')
        while len(self.players) < 2:
            time.sleep(2)
            if len(self.players) != players_last:
                self.log.info('New player connected, we are waiting for %s more player(s)',
                        2 - len(self.players))
                players_last = len(self.players)
            if not self.listener.is_alive():
                self.log.critical('Server listener died! Shutting down')
                return
        self.listener.shutdown() #We don't need this any more
        self.log.info('Players connected, starting game')
        self.prepare_players()
        p1 = self.players[0]
        p2 = self.players[1]
        for i in range(num_rounds):
            if not p1.is_alive or not p2.is_alive:
                self.log.critical('One or both of the players has closed their' +
                        ' connection to the game, aborting round. %s, %s', p1, p2)
                break
            self.log.debug('Starting round %i', i + 1)
            try:
                p1.new_game(num_rounds-i)
                p2.new_game(num_rounds-i)
                game = server_thread.ServerThread(p1, p2)
                game.run()
                winningPlayer, board = game.get_winner()
                if game.get_last_exception():
                    self.log.critical('Game threw exception:')
                    self.log.critical(game.get_last_exception())
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
                p1, p2 = p2, p1
                progress = int((float(i + 1) / num_rounds)*100)
                if progress % 10 == 0:
                    self.log.info('%s%% complete.', progress)
                time.sleep(1)#Had a problem where receiver did not get the message
                            #without this. Can be a local problem
            except:
                self.log.exception('An error occurred while trying to play')
                for p in self.players:
                    p.error()
                break
        self.shutdown()
        self.log.info('Played %i rounds', num_rounds)
        self.print_result()

    def print_result(self):
        self.log.info('Results:')
        for p1 in self.players:
            sum_rounds = self.wins[p1] + self.loses[p1] + self.ties[p1]
            if sum_rounds > 0:
                self.log.info('\t Player %s won %s times(%i%%), lost %s times(%i%%)' +
                        ' and tied %s times(%i%%)', str(p1),
                        self.wins[p1], (float(self.wins[p1])/sum_rounds)*100,
                        self.loses[p1], (float(self.loses[p1])/sum_rounds)*100,
                        self.ties[p1], (float(self.ties[p1])/sum_rounds)*100)

    def create_random_population(self, population, size):
        result = []
        pop = population[:]
        while len(pop) > size - 1:
            new_pop = random.sample(pop, size)
            for i in new_pop:
                pop.remove(i)
            result.append(new_pop)
        return result

    def play_continuous(self):
        self.log.info('Server starting continuous mode')
        self.listener.start()
        try:
            while True:
               if len(self.players) > 1:
                    players = self.players[:]
                    for p in players:
                        if not p.is_alive:
                            players.remove(p)
                            self.players.remove(p)
                            if len(players) == 0:
                                break
                            continue
                        else:
                            self.prepare_player(p)
                    self.log.info('Starting round with %i players', len(players))
                    play_threads = []
                    playing = self.create_random_population(players, 2)
                    self.log.info('Players playing this round: %r', playing)
                    for pair in playing:
                        t = server_thread.ServerThread(pair[0], pair[1])
                        try:
                            pair[0].new_game(1)
                            pair[1].new_game(1)
                        except:
                            self.log.debug('Player is not responding')
                            continue
                        t.start()
                        play_threads.append(t)
                    for thread in play_threads:
                        thread.join()
                        p1 = thread.p1
                        p2 = thread.p2
                        winner, board = thread.get_winner()
                        if not board:
                            #The thread has closed, likely because one of the players
                            #has quit the game
                            continue
                        if not winner:
                            self.ties[p1] += 1
                            self.ties[p2] += 1
                        else:
                            if winner == p1:
                                self.wins[p1] += 1
                                self.loses[p2] += 1
                            else:
                                self.wins[p2] += 1
                                self.loses[p1] += 1
                    self.log.info('Round completed, played %s game(s)', len(playing))
               else:
                   time.sleep(2)
        except:
            self.log.exception('Server threw exception while playing continuously')
        self.shutdown()
        self.print_result()
