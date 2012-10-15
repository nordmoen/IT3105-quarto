#!/usr/bin/python
import socket
import logging

from quarto.board import Board
from quarto.piece import Piece
from server import constants as const

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
        self.log.debug('Created network player with conn: %s and addr: %s',
                self.socket, self.addr)

    def new_game(self):
        '''Method used by the server to indicate that a new game is about to start
        this method will then inform the remote player'''
        self.log.debug('Sending new game message to remote player')
        self.socket.sendall(const.NEW_GAME)

    def get_piece(self, board, pieces):
        '''Method used by the server to indicate that it want the next piece from
        the remote player, this method will then contact the remote server and
        return the appropriate value'''
        self.log.debug('Sending get_piece message to remote player')
        self.socket.sendall(const.GET_PIECE)
        self.socket.sendall(repr(board.get_board()))
        self.socket.sendall(repr(map(lambda x: x.val, pieces)))
        piece = self.socket.recv(128)
        p = Piece(val=int(piece))
        self.log.debug('Got piece: %s(%r) from player:%s', p, p, piece)
        return p


    def get_placement(self, board, piece, pieces):
        '''Method used by the server to retrieve the next position that the
        remote player want to place the given piece in, this method will contact
        the remote player and relay the necessary information'''
        self.log.debug('Sending get_placement message to remote player')
        self.socket.sendall(const.GET_PLACEMENT)
        self.socket.sendall(repr(board.get_board()))
        self.socket.sendall(repr(piece.val))
        self.socket.sendall(repr(map(lambda x: x.val, pieces)))
        placement = eval(self.socket.recv(128))
        self.log.debug('Got placement: %r', placement)
        return placement

    def error(self, error=''):
        '''Method called by the server to tell a remote player that an error
        occurred and that it can no longer send or receive more messages'''
        self.log.warning('Sending error message to player')
        self.socket.sendall(const.ERROR)

    def __str__(self):
        return 'Network player, Conn{}, Addr:{}'.format(self.socket, self.addr)
