# Airline Seating Assignment
[Peter Adam](https://github.com/Padam-0) & [Andy McSweeney](https://github.com/mcsweena)


## Software Specification
seat_assign_16201859_16203177.py is a software algorithm to allocate seats 
on an airline when passengers make bookings, and write them to a database. For 
each flight, seats are allocated to passengers, and bookings of multiple 
passengers are allocated seats together where possible.

Each flight is different, and the algorithm can deal with different airline 
configurations, as contained in the flight database.

The bookings take the form of a .CSV where each line consists of one 
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
where data.db is the flight database and bookings.csv is the .CSV of bookings.



### Database Cleaning

This option is specified from the command line by calling:
`python seat_assign_16201859_16203177.py clean data.db`
where data.db is the flight database.

This function will set all seats in the seating table to empty, and reset 
metrics to 0. rows_cols will be untouched.


### Flight Creation

This option is specified from the command line by calling:
`python seat_assign_16201859_16203177.py create data.db rows seats`
where data.db is the flight database, rows is the number of rows(ie 10) and 
seats is the seating configuration (ie ABCDEF).

The flight database can either be existing (but completely empty) or 
non-existing.

This function will create a database, populate the rows_cols table with the 
specified number of rows and columns, initialise the metrics table to 0, and
 populate the `seating` table with all seat combinations, and set these 
 seats to empty.

