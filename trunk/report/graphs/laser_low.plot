set term postscript eps 
set output "laser_low.eps"
set title "Laser Detection in Low Light"
set size 0.55,0.55
set grid
set xtics 5
set xrange [0:25]
set style fill pattern
set boxwidth 2 
set yrange [0:20]
set ylabel "Failure Rate (%)"
set xlabel "Distance (feet)"
set key top left
plot "graphs/laser_low.txt" using ($1-1):2 title 'Green Moving Laser' with boxes, "graphs/laser_low.txt" using ($1+1):3 title 'Red Stationary Laser' with boxes

