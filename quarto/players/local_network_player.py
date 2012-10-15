#!/usr/bin/python

import logging
import socket
from server import constants as const

class LocalNetworkPlayer(object):
    '''Network player used when starting a player who is going to connect to
    a remote server'''

    def __init__(self, addr, port, player, log=None):
        self.addr = addr
        self.port = port
        self.player = player
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
        while True:
            move = self.socket.recv(128)
            if move == const.NEW_GAME:
                self.log.debug('Got new_game message from server reseting player')
                self.player.reset()
            elif move == const.ERROR:
                self.log.debug('Got error message from server quiting')
                break
            elif move == const.GET_PIECE:
                self.log.debug('Got get_piece message from server')
                message = self.socket.recv(4096)
                self.log.debug('Got message from server: %s', message)
                self.log.debug('Got board: %s', message[0])
                self.log.debug('Got these pieces from server: %s', message[1])
                ret = self.player.get_piece(b, map(lambda x: Piece(val=x), eval(pieces)))
                self.log.debug('Sending %s(%r) to server', ret, ret)
                self.socket.sendall(repr(ret.val))
            elif move == const.GET_PLACEMENT:
                self.log.debug('Got get_piece message from server')
                board = eval(self.socket.recv(4096))
                self.log.debug('Got board: %s', board)
                piece = eval(self.socket.recv(128))
                p = Piece(val=piece)
                self.log.debug('Got piece %s(%r)', p, p)
                pieces = eval(self.socket.recv(4096))
                self.log.debug('Got these pieces from server: %s', pieces)
                placement = self.player.get_placement(board, p, map(lambda x: Piece(val=x),
                    eval(pieces)))
                self.log.debug('Sending %s as placement to server', placement)
                self.socket.sendall(repr(placement))

    def __str__(self):
        return 'LocalNetwork Player: {}, Connection: {}:{}'.format(self.player,
                self.addr, self.port)
