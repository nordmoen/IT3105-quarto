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
        self.is_alive = True

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
        sending_pieces = map(lambda x: x.val, pieces)
        self.socket.sendall(const.GET_PIECE + '\n' + repr(sending_pieces))
        piece = self.socket.recv(128)
        p = Piece(val=int(piece))
        self.log.debug('Got piece: %s(%r) from player', p, p)
        return p

    def translate_pos(self, pos):
        '''Translate a position of the format (x, y) to the format
        [0, 1, 2, 3]
        [4, 5, 6, 7]
        [8, 9, 10, 11]
        [12, 13, 14, 15]'''
        return pos[1]*4 + pos[0]

    def translate_int_pos(self, i):
        '''Translate from int:
        [0, 1, 2, 3] ...
        to (x, y)'''
        x = i % 4
        y = (i-x) / 4
        return (x, y)

    def piece_placed(self, piece, pos):
        self.log.debug('Sending piece_placed message to remote player')
        self.socket.sendall(const.PIECE_PLACED + '\n' + repr(piece.val) + '\n' +
                repr(self.translate_pos(pos)))

    def get_placement(self, board, piece, pieces):
        '''Method used by the server to retrieve the next position that the
        remote player want to place the given piece in, this method will contact
        the remote player and relay the necessary information'''
        self.log.debug('Sending get_placement message to remote player')
        self.socket.sendall(const.GET_PLACEMENT + '\n' + repr(piece.val))
        placement = self.socket.recv(128)
        self.log.debug('Got placement: %r', placement)
        return self.translate_int_pos(int(placement))

    def error(self, error=''):
        '''Method called by the server to tell a remote player that an error
        occurred and that it can no longer send or receive more messages'''
        self.log.warning('Sending error message to player')
        self.socket.sendall(const.ERROR)
        self.__shutdown()

    def shutdown(self):
        self.log.debug('Sending shutdown message')
        self.socket.sendall(const.SHUTDOWN)
        self.__shutdown()

    def __shutdown(self):
        self.is_alive = False
        self.log.debug('Shutingdown socket')
        try:
            self.socket.close()
        except:
            self.log.exception('Exception happened while trying to close socket')



    def __str__(self):
        alive_msg = 'Alive' if self.is_alive else 'Dead'
        return 'Network player({}), Conn{}, Addr:{}'.format(alive_msg,
                self.socket, self.addr)
