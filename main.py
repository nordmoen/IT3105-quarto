#!/usr/bin/python

import argparse
from quarto import quarto

def play_quarto(args):
    print args

def start_server(args):
    pass

def main():
    parser = argparse.ArgumentParser(description='Start up a game of Quarto')
    mode_parsers = parser.add_subparsers(title='Modes', 
            description='Possible modes to start', help='Additional help')
    game_mode = mode_parsers.add_parser('game', help='Start a Quarto game')
    game_mode.add_argument('-r', '--rounds', default=1, type=int, 
            help='The number of rounds to be played')
    game_mode.add_argument('-s', '--simulate', action='store_true', 
            help='Should the game be simulated, i.e. should the game print final statistics')
    
    game_mode.set_defaults(func=play_quarto)

    server_mode = mode_parsers.add_parser('server', help='Start a Quarto server')
    server_mode.add_argument('-p', '--port', default=49455, type=int, 
            help='Select the port to start the server on')
    server_mode_group = server_mode.add_mutually_exclusive_group(required=True)
    server_mode_group.add_argument('--continuous', action='store_true', 
            help='Run the server continuously and let players connect and disconnect while playing')
    server_mode_group.add_argument('--game', action='store_true',
            help='Start the server in game mode and wait for two players to connect and player Quarto')
    server_mode.add_argument('--rounds', default=1, type=int, 
            help='Number of rounds to play if "--game" is selected')
    server_mode.set_defaults(func=start_server)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
