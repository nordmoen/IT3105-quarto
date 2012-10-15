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
        self.log.debug('Connected to server ready to play')

    def play(self):
        '''Method used to start this player playing games with the server.
        This method is used when the user starts this class from the command-line'''
        if not self.player or not self.socket:
            self.log.critical('Can not call method play without first calling' +
                    ' connect successfully')
            return
        board = None
        pieces = None
        while True:
            move = self.socket.recv(4096).split('\n')
            if move == const.NEW_GAME:
                self.log.debug('Got new_game message from server reseting player')
                board = Board()
                pieces = {i:Piece(val=i) for i in range(16)}
                self.player.reset()
            elif move[0] == const.ERROR:
                self.log.debug('Got error message from server quiting')
                break
            elif move[0] == const.GET_PIECE:
                self.log.debug('Got get_piece message from server: %s', move)
                next_piece = self.player.get_piece(board, pieces)
                self.log.debug('Sending piece: %s(%r) to server', next_piece)
                self.socket.sendall(next_piece.val)
            elif move[0] == const.GET_PLACEMENT:
                self.log.debug('Got get_piece message from server: %s', move)
                del pieces[int(move[1])]
                pos = self.player.get_placement(board, Piece(val=int(move[1])), pieces)
                self.log.debug('Sending pos %s to server', pos)
                self.socket.sendall(repr(self.translate_pos_int(pos)))
            elif move[0] == const.PIECE_PLACED:
                self.log.debug('Got place_piece message from server: %s', move)
                board.place(Piece(val=int(move[1])), *self.translate_int_pos(int(move[2])))
            elif move[0] == const.SHUTDOWN:
                self.log.debug('Got shutdown message')
                break
        self.__shutdown()

    def __shutdown(self):
        self.log.debug('Shuting down socket')
        try:
            self.socket.close()
        except:
            self.log.exception('Got exception trying to close socket')

    def __str__(self):
        return 'LocalNetwork Player: {}, Connection: {}:{}'.format(self.player,
                self.addr, self.port)
