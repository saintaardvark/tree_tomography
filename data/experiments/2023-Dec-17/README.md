# December 17, 2023

Using log for first time.  Sensor at top and bottom, both sides.

Using hammer by holding it on side A by hand, sensor 1 -- travel time to sensor 2.

Have marked places where feet of hammer can be put so that we can try
to get consistent measurements.

* **NOTE:** I realized afterward that this meant we were likely
  putting the back end of the hammer on the protective board of the
  other sensor.  Eg: if we were banging on sensor 1, the back of the
  hammer was probably resting on sensor 2.  There may have been some
  mechanical coupling here; it would be good to avoid this next time.

# First running

Sensor 1 to Sensor 2

2023-12-17_14:16:15.csv -- first run, no holes. 
2023-12-17_14:18:30.csv -- second run, no holes

-> combined: first_run_1_to_2.csv

Sensor 2 to Sensor 1

2023-12-17_14:24:06.csv -- first run, no holes
2023-12-17_14:25:33.csv -- second run,no holes.  Removed 4 outliers (hundreds of thousands of microseconds)

-> combined: first_run_2_to_1.csv

# Second run

one hole, 3.25" deep, middle

Sensor 1 to Sensor 2

2023-12-17_14:40:22.csv -- first run, one hole
2023-12-17_14:41:43.csv -- second run, one hole

-> combined: second_run_1_to_2.csv

Sensor 2 to Sensor 1

2023-12-17_14:43:41.csv -- first run, one hole; removed one outlier at start
2023-12-17_14:45:00.csv -- second run, one hole

-> combined: second_run_2_to_1.csv 

Hole 1" across.  Radius of whole log is 6".  Hole is approx in middle -- so call it a 1.67% increase in difference

Going to drill 2 more holes to make larger diff -- figure should be approx 11.6% further, which hopefully will show up with larger time of flight values.

# Third run

3 holes!  About 2.75" across.

1 -> 2

- Had to tighten clamp & move it up so it poked above level of log -- otherwise, hammer didn't hit it

2023-12-17_15:07:40.csv -- first run, three holes
2023-12-17_15:09:55.csv -- second run

-> combined: third_run_1_to_2.csv

2 -> 1

2023-12-17_15:14:30.csv -- first run
2023-12-17_15:15:26.csv -- second run

-> combined: third_run_2_to_1.csv

# Fourth run

1 -> 3, 3 holes (though not in path of 1-3)

Log: ~ 15 " long.  11" between sensors

2023-12-17_15:18:43.csv -- first run, one outlier removed
2023-12-17_15:21:32.csv -- second run

# Fifth run

2->4
had to replace sensor 4, because was not sensitive enough

2023-12-17_15:32:30.csv -- first run

# Sixth run

Move board for sensor 1 so now poking up above log level -- hopefuly to get more consistent hit from hammer

Sensor 1-2 

2023-12-17_15:40:39.csv -- first run

Sensor 2->1
2023-12-17_15:42:51.csv -- first run
