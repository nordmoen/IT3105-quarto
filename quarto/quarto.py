#!/usr/bin/python

from game import Game

def main(player1, player2, num_rounds, simulate=False):
    game = Game(player1, player2)
    res = [0,0]
    for i in range(num_rounds):
        winner, board, win_pos, last_placed_pos = game.play()
        if winner:
            res[winner - 1] += 1
        if not simulate:
            print_game_stats(player1, player2, winner, board, win_pos, last_placed_pos)
    if simulate:
        print 'Game statistics:'
        print 'Total games played: {}'.format(num_rounds)
        print 'Player 1 won: {}'.format(res[0])
        print 'Player 2 won: {}'.format(res[1])
        print 'Ties: {}'.format(num_rounds-sum(res))

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
