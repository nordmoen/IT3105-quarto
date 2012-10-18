#!/usr/bin/python

import threading
import socket
import logging
from quarto.players import network_player
import constants as const

class ServerListener(threading.Thread):
    '''This class represent a thread which will be listening for
    incoming request to join the server and will add those requesting
    to a list of players which the server can use to start games'''

    def __init__(self, player_list, bind_addr, port, log = None):
        threading.Thread.__init__(self)
        self.p_list = player_list
        self.listen = True
        self.socket = None
        self.addr = bind_addr
        self.port = port
        if log:
            self.log = log
        else:
            self.log = logging.getLogger(self.__class__.__name__)

    def run(self):
        self.log.debug('Creating socket')
        self.socket = socket.socket() #Default ipv4 and TCP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind((self.addr, self.port))
        except:
            self.log.exception('Could not bind socket to address: %s:%i', self.addr, self.port)
            self.log.critical('Shutting down after socket error')
            return
        self.log.info('Socket bound to address: %s:%i', *(self.socket.getsockname()[:2]))
        try:
            self.socket.listen(1)
        except:
            self.log.exception('Could not get socket to listen')
            return
        while self.listen:
            self.log.debug('Waiting for connection')
            try:
                conn, addr = self.socket.accept()
            except:
                self.log.warning('Socket accept threw exception')
                self.shutdown()
                break
            self.log.debug('Got connection from address "%s"', addr)
            hello_msg = conn.recv(128)
            if hello_msg == const.HELLO:
                conn.sendall(const.HELLO)
                self.log.debug('Creating new network player')
                player = network_player.NetworkPlayer(conn, addr)
                self.log.debug('Adding new player to the list')
                self.p_list.append(player)
        self.log.info('Server listener shut down completed')

    def shutdown(self):
        self.log.info('Shutting down listener')
        self.listen = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                self.log.debug('Shutdown threw error while shutting down')
            try:
                self.socket.close()
            except:
                self.log.exception('Could not shutdown socket')
