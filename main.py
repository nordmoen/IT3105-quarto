#!/usr/bin/python

import argparse
import logging
from quarto import quarto
from quarto.players import random_player, human_player, novice_player, minimax_player, network_player
from server import server

def play_quarto(args):
    p1 = create_player(args.player1)
    p2 = create_player(args.player2)
    quarto.main(p1, p2, args.rounds, args.simulate)

def start_network_player(args):
    print args

def start_server(args):
    logging.basicConfig(level=getattr(logging, args.log))
    serv = server.Server(args.addr, args.port)

def create_player(args):
    type = args[0]
    if type == 'random':
        return random_player.RandomPlayer()
    elif type == 'novice':
        return novice_player.NovicePlayer()
    elif type == 'human':
        return human_player.HumanPlayer()
    elif type == 'minimax':
        try:
            difficulty = int(args[1])
            if len(args) > 2:
                when_to_change = int(args[2])
            else:
                when_to_change = 2
            return minimax_player.MinimaxPlayer(difficulty, when_to_change)
        except IndexError:
            print 'No difficulty selected for player!'
            raise
    else:
        raise TypeError('Player type needs to be the first argument to a player')


def main():
    parser = argparse.ArgumentParser(description='Start up a game of Quarto')
    mode_parsers = parser.add_subparsers(title='Modes',
            description='Possible modes to start', help='Additional help')
    game_mode = mode_parsers.add_parser('game', help='Start a Quarto game')
    game_mode.add_argument('-r', '--rounds', default=1, type=int,
            help='The number of rounds to be played')
    game_mode.add_argument('-s', '--simulate', action='store_true',
            help='Should the game be simulated, i.e. should the game print final statistics')
    game_mode.add_argument('--player1', nargs='+', default='random', choices=['random',
        'novice', 'minimax', 'human'].extend(range(10)), required=True,
        help='Select the type of player 1, if minimax is chosen an additional argument is needed')
    game_mode.add_argument('--player2', nargs='+', default='random', choices=['random',
        'novice', 'minimax', 'human'].extend(range(10)), required=True,
        help='Select the type of player 2, if minimax is chosen an additional argument is needed')

    game_mode.set_defaults(func=play_quarto)

    server_mode = mode_parsers.add_parser('server', help='Start a Quarto server')
    server_mode.add_argument('-p', '--port', default=49455, type=int,
            help='Select the port to start the server on')
    server_mode.add_argument('-a', '--addr', default='localhost',
            help='Select the address which the server should bind to')
    server_mode_group = server_mode.add_mutually_exclusive_group(required=True)
    server_mode_group.add_argument('--continuous', action='store_true',
            help='Run the server continuously and let players connect and disconnect while playing')
    server_mode_group.add_argument('--game', action='store_true',
            help='Start the server in game mode and wait for two players to connect and player Quarto')
    server_mode.add_argument('--rounds', default=1, type=int,
            help='Number of rounds to play if "--game" is selected')
    server_mode.add_argument('--log', default='INFO', choices=['DEBUG',
        'INFO', 'WARNING', 'CRITICAL'], help='Select the level at which the' +
        ' logging should emit messages, everything below the selected level will also be printed')
    server_mode.set_defaults(func=start_server)

    network_mode = mode_parsers.add_parser('network', help='Start a network player to connect to a server')
    network_mode.add_argument('type', nargs='+', default='novice', choices=['random',
        'novice', 'minimax', 'human'].extend(range(10)),
        help='Select the type of the network player,' +
        ' if minimax is chosen an additional argument is needed')
    network_mode.add_argument('-a', '--addr', default='localhost',
            help='Select the address which the server should bind to')
    network_mode.add_argument('-p', '--port', default=49455, type=int,
            help='Select the port to start the server on')
    network_mode.set_defaults(func=start_network_player)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
