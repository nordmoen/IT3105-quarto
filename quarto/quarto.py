#!/usr/bin/python

from time import time
from game import Game

def main(player1, player2, num_rounds, simulate=False):
    game = Game(player1, player2)
    res = {player1: 0, player2: 0}
    progress = 0
    mod_games = num_rounds / 10.0
    for i in range(num_rounds):
        winner, board, win_pos, last_placed_pos = game.play()
        player1.reset()
        player2.reset()
        if winner:
            res[winner] += 1
        if not simulate:
            print_game_stats(player1, player2, winner, board, win_pos, last_placed_pos)
        if i % 2 == 0:
            game = Game(player2, player1)
        else:
            game = Game(player1, player2)

        if num_rounds >= 10 and i % (num_rounds/10.0) == 0:
            print '{}% complete.'.format(progress*10)
            progress += 1
    print '100% complete.'

    if simulate:
        print 'Game statistics:'
        print 'Total games played: {}'.format(num_rounds)
        print 'Player {} won: {}, {}%'.format(player1, res[player1],
                int((float(res[player1])/num_rounds)*100))
        print 'Player {} won: {}, {}%'.format(player2, res[player2],
                int((float(res[player2])/num_rounds)*100))
        print 'Ties: {}'.format(num_rounds-(res[player1] + res[player2]))

def print_game_stats(player1, player2, winner, board, win_pos, last):
    if winner == 1:
        print 'Player 1 won the game!'
    else:
        print 'Player 2 won the game!'
    if win_pos[0] == 1 and not win_pos[1]:
        print 'The player won horizontally on row {}'.format(last[1])
    elif win_pos[1] == 1 and not win_pos[0]:
        print 'The player won vertically on column {}'.format(last[0])
    elif win_pos[0] == 3:
        print 'The player won on the diagonal from right to left'
    else:
        print 'The player won on the diagonal from left to right'
    print board
