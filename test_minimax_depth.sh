#!/usr/bin/bash

for i in {2..10..2}
do
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 2 -r 500 -s >> minimax2.txt &
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 4 -r 500 -s >> minimax4.txt &
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 6 -r 500 -s >> minimax6.txt &
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 8 -r 500 -s >> minimax8.txt &
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 10 -r 500 -s >> minimax10.txt &
	time python main.py game --player1 minimax 3 $i --player2 minimax 3 12 -r 500 -s >> minimax12.txt
done
