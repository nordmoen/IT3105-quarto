#Gnuplot script to graph out the plot for when minimax should switch
#Data is inside minimax.dat

set terminal postscript eps monochrome dashed lw 2
set title "Comparison of when Minimax player should switch from novice to minimax"
set xlabel "Against Minimax player switching after"
set ylabel "Percentage of wins"
set offset graph 0.05, graph 0.05
set yrange [0:1]
set output "switch.eps"
set xtics (2,4,6,8,10)

#The plotting commands:
plot "minimax.dat" using 1:($2/500) title "Minimax depth:3, switch: 2" with lines, \
"minimax.dat" using 1:($3/500) title "Minimax depth:3, switch: 4" with lines, \
"minimax.dat" using 1:($4/500) title "Minimax depth:3, switch: 6" with lines, \
"minimax.dat" using 1:($5/500) title "Minimax depth:3, switch: 8" with lines, \
"minimax.dat" using 1:($6/500) title "Minimax depth:3, switch: 10" with lines, \
"minimax.dat" using 1:($7/500) title "Minimax depth:3, switch: 12" with lines
