# Airline Seating Assignment
[Peter Adam](https://github.com/Padam-0) - [16201859](mailto:peter.adam@ucdconnect.ie)  
[Andy McSweeney](https://github.com/mcsweena) - [16203117](mailto:andy.mcsweeney@ucdconnect.ie)


## Software Specification
`seat_assign_16201859_16203177.py` is a software algorithm to allocate seats 
on an airline when passengers make bookings, and write them to a database. For 
each flight, seats are allocated to passengers, and bookings of multiple 
passengers are allocated seats together where possible.

Each flight is different, and the algorithm can deal with different airline 
configurations, as contained in the flight database.

The bookings take the form of a `.CSV` where each line consists of one 
integer representing the name of the person making the booking and number of 
passengers in the party. Seats are allocated in booking order.

## Use

The software has three main usages:

1. Allocate Seats from a booking file;
2. Clean a flight database to an empty form; and
3. Create a flight database for new planes.

### Seat Allocation

This option is specified from the command line by calling:  
  
`python seat_assign_16201859_16203177.py data.db bookings.csv`  
  
where `data.db` is the flight database and `bookings.csv` is the `.CSV` file
 of bookings.

A list of bookings will be printed to the command line with the booking name 
and number of passengers in the booking, as well as a statement about 
whether the party was seated or refused. If the party was seated but split, 
multiple lines indicate the seating plan for that party.

After all bookings have been processed, 3 summary statistics are printed. 
The first contains the total number of passengers seated. The second shows 
how many parties were split, and the last contains the total number of 
passengers who were refused entry.

Parties split refers to the number of ways the booking was split in order to 
accomodate all passengers. As such, a 4 person booking that was split 2,2 is 
recorded as a 1 party split, but a 5 person booking that was split 3,1,1 is 
recorded as a 2 party split.

If there are more passengers in a booking than there are empty seats on the 
plane, the entire booking is refused and seats filled with subsequent 
(smaller) bookings.


### Database Cleaning

This option is specified from the command line by calling:  
  
`python seat_assign_16201859_16203177.py clean data.db`  
  
where `data.db` is the flight database.

This function will set all seats in the `seating` table to empty, and reset 
`metrics` to `0`. `rows_cols` will be untouched.


### Flight Creation

This option is specified from the command line by calling:  
`python seat_assign_16201859_16203177.py create data.db rows seats`  
where `sata.db` is the flight database, `rows` is the number of rows(ie `10`) 
and `seats` is the seating configuration (ie `ABCDEF`).

The flight database can exist (but must be completely empty) or 
will be created by the function.

This function will create a database, populate the `rows_cols` table with the 
specified number of rows and columns, initialise the `metrics` table to `0`, 
and populate the `seating` table with all seat combinations, and set these 
seats to empty.

