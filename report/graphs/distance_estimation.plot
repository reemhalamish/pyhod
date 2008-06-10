set term postscript eps
set output "distance_estimation.eps"
set title "Distance Estimation"
set size 0.55,0.55
set grid
set xtics 1 
set xrange [0:9]
set style fill pattern
set boxwidth 2 
set yrange [0:30]
set ylabel "Error (%)"
set xlabel "Distance from Wall (feet)"
set key top left
plot "graphs/distance_estimation.txt" using 1:(100*(($1-$2)/$1)) title 'Estimation Error' with lines 

