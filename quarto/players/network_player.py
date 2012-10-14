#!/usr/bin/python
import socket
import logging

from quarto.board import Board
from server.constants import *

class NetworkPlayer(object):
    '''Network player to work together with our quarto game implementation.'''

    def __init__(self, conn, addr, log=None):
        if log:
            self.log = log
        else:
            self.log = logging.getLogger('{} conn:{}, addr:{}'.format(
                self.__class__.__name__, conn, addr))
        self.socket = conn
        self.addr = addr
        self.log.debug('Created network player with conn: %s and addr %s',
                self.socket, self.addr)


    def connect(self, port, player, timeout):
        '''Method to connect to a server. This method is used when a user want
        to start the player from the command-line to connect to a server'''
        if self.socket:
            self.log.critical('Can not create a new connection because this player' +
                    ' is already connected to %s!', self.socket)
            return
        if not player:
            self.log.critical('Can not connect to server without a proper player ' +
                    'to play with')
            return
        self.player = player
        self.log.debug('Connecting to server')
        try:
            self.socket = socket.create_connection((self.addr,
                port), timeout if timeout else socket.getdefaulttimeout())
        except:
            self.log.exception('Could not establish connection with %s:%i',
                    self.addr, port)
            return
        for i in range(2):
            self.log.debug('Trying to say hello to server, round %i', i)
            self.socket.sendall(HELLO)
            respons = self.socket.recv(128)
            if respons == HELLO:
                self.log.debug('Server said hello back!')
                break
        else:
            raise socket.error('Could not get a proper response from the server')
        #If we get here we have connected to the server and said hello to it
        self.log.debug('Connected to server ready to play')

    def play(self):
        '''Method used to start this player playing games with the server.
        This method is used when the user starts this class from the command-line'''
        if not self.player:
            self.log.critical('Can not call method play without first calling' +
                    ' connect')
            return
        pass

    def new_game(self):
        '''Method used by the server to indicate that a new game is about to start
        this method will then inform the remote player'''
        pass

    def get_piece(self, board, pieces):
        '''Method used by the server to indicate that it want the next piece from
        the remote player, this method will then contact the remote server and
        return the appropriate value'''
        pass

    def get_placement(self, board, piece, pieces):
        '''Method used by the server to retrieve the next position that the
        remote player want to place the given piece in, this method will contact
        the remote player and relay the necessary information'''
        pass

    def error(self):
        '''Method called by the server to tell a remote player that an error
        occurred and that it can no longer send or receive more messages'''
        pass

    def __str__(self):
        if self.player:
            return 'Network player, Conn:{}, Addr:{}, Player:{}'.format(self.socket,
                    self.addr, self.player)
        else:
            return 'Network player, Conn{}, Addr:{}'.format(self.socket, self.addr)
