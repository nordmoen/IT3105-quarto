#!/usr/bin/python

import logging
import socket
from quarto.piece import Piece
from quarto.board import Board
from server import constants as const

class LocalNetworkPlayer(object):
    '''Network player used when starting a player who is going to connect to
    a remote server'''

    def __init__(self, addr, port, player, log=None):
        self.addr = addr
        self.port = port
        self.player = player
        self.socket = None
        if not log:
            self.log = logging.getLogger(self.__class__.__name__)
        else:
            self.log = log

    def connect(self, timeout=None):
        '''Method to connect to a server. This method is used when a user want
        to start the player from the command-line to connect to a server'''
        if not self.player:
            self.log.critical('Can not connect to server without a proper player ' +
                    'to play with')
            return
        self.log.debug('Connecting to server: %s:%i', self.addr, self.port)
        try:
            self.socket = socket.create_connection((self.addr,
                self.port), timeout if timeout else socket.getdefaulttimeout())
        except:
            self.log.exception('Could not establish connection with %s:%i',
                    self.addr, self.port)
            return
        for i in range(2):
            self.log.debug('Trying to say hello to server, round %i', i)
            self.socket.sendall(const.HELLO)
            respons = self.socket.recv(128)
            if respons == const.HELLO:
                self.log.debug('Server said hello back!')
                break
        else:
            raise socket.error('Could not get a proper response from the server')
        #If we get here we have connected to the server and said hello to it
        self.log.info('Connected to server ready to play')

    def play(self):
        '''Method used to start this player playing games with the server.
        This method is used when the user starts this class from the command-line'''
        if not self.player or not self.socket:
            self.log.critical('Can not call method play without first calling' +
                    ' connect successfully')
            return
        self.board = None
        self.games = 0
        self.total_games = 0
        self.mod_games = 0
        self.pieces = None
        while True:
            move = self.socket.recv(512).split()
            self.log.debug('Got message: %r', move)
            self.log.debug('Board:\n%s', self.board)
            self.log.debug('Pieces: %s', self.pieces)
            if not self.handle_message(move):
                break
        self.__shutdown()

    def handle_message(self, message):
        move = message[0]
        if move[0] == const.NEW_GAME:
            self.log.debug('Got new_game message from server reseting player')
            self.board = Board()
            self.pieces = {i:Piece(val=i) for i in range(16)}
            self.player.reset()
            games_left = int(move[1])
            if self.total_games == 0:
                self.log.debug('Updating total_games to: %s', games_left)
                self.total_games = games_left
                self.mod_games = int(self.total_games / 10.0)
            if self.mod_games > 0:
                if self.games % self.mod_games == 0:
                    self.log.info('We are %i%% complete!', (self.games / float(self.total_games))*100)
            self.games += 1
        elif move[0] == const.ERROR:
            self.log.warning('Got error message from server quiting')
            return False
        elif move[0] == const.GET_PIECE:
            self.log.debug('Got get_piece message from server: %s', move)
            next_piece = self.player.get_piece(self.board, self.pieces.values())
            self.log.debug('Sending piece: %s(%r) to server', next_piece, next_piece)
            self.socket.sendall(repr(next_piece.val))
        elif move[0] == const.GET_PLACEMENT:
            self.log.debug('Got get_placement message from server: %s', move)
            piece = int(move[1])
            if piece in self.pieces:
                del self.pieces[piece]
            pos = self.player.get_placement(self.board, Piece(val=piece), self.pieces.values())
            self.log.debug('Sending pos %s to server', pos)
            self.socket.sendall(repr(self.translate_pos_int(pos)))
        elif move[0] == const.PIECE_PLACED:
            self.log.debug('Got placed_piece message from server: %s', move)
            piece = int(move[1])
            if piece in self.pieces:
                del self.pieces[piece]
            self.board.place(Piece(val=int(move[1])), *self.translate_int_pos(int(move[2])))
        elif move[0] == const.SHUTDOWN:
            self.log.info('Got shutdown message')
            results = map(int, move[1:])
            total = sum(results)
            self.log.info('Wins: %s(%i%%)', move[1], (results[0] / float(total))*100)
            self.log.info('Loses: %s(%i%%)', move[2], (results[1] / float(total))*100)
            self.log.info('Ties: %s(%i%%)', move[3], (results[2] / float(total))*100)
            return False
        if len(message) > 1:
            return self.handle_message(message[1:])
        return True

    def translate_int_pos(self, i):
        '''Translate from int:
        [0, 1, 2, 3] ...
        to (x, y)'''
        x = i % 4
        y = (i-x) / 4
        return (x, y)

    def translate_pos_int(self, pos):
        return pos[1]*4 + pos[0]

    def __shutdown(self):
        self.log.debug('Shuting down socket')
        try:
            self.socket.close()
        except:
            self.log.exception('Got exception trying to close socket')

    def __str__(self):
        return 'LocalNetwork Player: {}, Connection: {}:{}'.format(self.player,
                self.addr, self.port)
