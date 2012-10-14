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
        self.log.debug('Connecting to server: %s:%i', self.addr, port)
        try:
            self.socket = socket.create_connection((self.addr,
                port), timeout if timeout else socket.getdefaulttimeout())
        except:
            self.log.exception('Could not establish connection with %s:%i',
                    self.addr, port)
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
        if self.player:
            return 'Network player, Conn:{}, Addr:{}, Player:{}'.format(self.socket,
                    self.addr, self.player)
        else:
            return 'Network player, Conn{}, Addr:{}'.format(self.socket, self.addr)
