set xrange [-1:1]
set yrange [0:1.1]

set arrow from 0.1,0 to 0,1 nohead lt -1 
set arrow from -0.1,0 to 0,1 nohead lt -1
set label 1 "Center" at -.055,1.025 
 
set arrow from -0.4,0 to ((-0.4-0.05)/2),1 nohead lt 1
set arrow from ((-0.4-0.05)/2),1 to -0.05,0 nohead lt 1 
set label 2 "Slight Neg" at -0.33,1.025 

set arrow from -0.7,0 to ((-0.7-0.3)/2),1 nohead lt 2
set arrow from ((-0.7-0.3)/2),1 to -0.3,0 nohead lt 2
set label 3 "Negative" at -0.58,1.025 

set arrow from -1,1 to -0.9,1 nohead lt 3
set arrow from -0.9,1 to -0.5,0 nohead lt 3
set label 4 "Far Negative" at -.97,1.025 
