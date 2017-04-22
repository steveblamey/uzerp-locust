reset
set datafile separator ","

# Get the mean and standard deviation
plot './stats.csv' using 0:4
set yrange [0:4]
f(x) = mean_y
fit f(x) './stats.csv' u 0:4 via mean_y
stddev_y = sqrt(FIT_WSSR / (FIT_NDF + 1 ))

# Plot the chart
set autoscale
set ylabel 'Response Time (ms)'
set title 'uzERP Locust Run, Finished: '.strftime("%a %b %d %H:%M:%S %Y", time(0))
plot './stats.csv' u 0:4 w p pt 7 lt 1 ps 1 notitle, \
mean_y title gprintf("Mean = %g", mean_y), \
stddev_y*3 title gprintf("3 x Std. dev. = %g", stddev_y*3)


