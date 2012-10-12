#!/usr/bin/python
import socket
import logging

from ..board import Board

HELLO = '07734'
NEW_GAME = '3049'
ERROR = '20223'

class NetworkPlayer(object):
    '''Network player to work together with our quarto game implementation.'''

    def __init__(self, ip, port, timeout, player, log=None):
        if log:
            self.log = log
        else:
            self.log = logging.getLogger('Network player {}:{}, class: {}'.format(ip,
                port, player))
        self.player = player
        #Connect to the server and do handshake
        self.log.debug('Connecting to server')
        self.socket = socket.create_connection((ip, port), timeout) if timeout else socket.getdefaulttimeout()
        for i in range(2):
            self.log.debug('Trying to say hello to server, round %i', i)
            self.socket.sendall(HELLO)
            respons = self.socket.recv(32)
            if respons == HELLO:
                self.log.debug('Server said hello back!')
                break
        else:
            raise socket.error('Could not get a proper respons from the server')
        #If we get here we have connected to the server and said hello to it
        self.log.debug('Connected to server ready to play')
        
    def play(self):
        self.log.debug('Starting to play')
        games = 0
        wins = 0
        ties = 0
        play = True
        while play:
            self.log.debug('Waiting for new game from server')
            start_game = self.socket.recv(1024)
            if start_game == NEW_GAME:
                self.log.debug('Starting new game')
                while True:
                    server_resp = self.socket.recv(1024)
                    if server_resp == GET_PICE:
                        pass
                    elif server_resp == GET_PLACEMENT:
                        pass
                    elif server_resp == ERROR:
                        play = False
                        break
                    else:
                        raise socket.error('Got weird respons from server: {}'.format(server_resp))
            else:
                break
        win_perce = int(float(wins)/games)*100
        ties_perce = int(float(ties)/games)*100
        lose_perce = 100 - win_perce - ties_perce
        self.log.info('Played %i games', games)
        self.log.info('Won %i games, %i%', wins, win_perce)
        self.log.info('Tied %i games, %i%', ties, ties_perce)
        self.log.info('Lost %i games, %i%', games - (wins + ties), lose_perce)
