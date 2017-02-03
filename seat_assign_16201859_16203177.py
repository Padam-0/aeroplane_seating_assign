from sqlalchemy import create_engine
import sys


def organize_booking(booking_name, pas_in_booking, empty_seats_per_row,
        empty_seats, cols, engine):
    pass


def retrieve_data(engine, rows, cols):
    # Connect to database and retrieve a list of empty seats and metric
    # information

    with engine.connect() as con:
        empty_seats = con.execute("SELECT * FROM seating WHERE name "
                                  "='';").fetchall()
        metrics = con.execute('SELECT * FROM metrics;').fetchall()[0]

    # Define metrics:
    num_pas_refused, num_pas_split = metrics[0], metrics[1]

    # Create list of empty seats per row
    empty_seats_per_row = {}
    for row in range(rows):
        empty_seats_in_row = 0
        for col in cols:
            if (row + 1, col, '') in empty_seats: empty_seats_in_row += 1
        empty_seats_per_row[row + 1] = empty_seats_in_row

    return empty_seats, empty_seats_per_row, num_pas_refused, num_pas_split


def find_row_with_n_empty_seats(empty_seats_per_row, number_of_pas, e):
    # Finds a row which has a number of empty seats (number of passengers
    # plus the constant e), if one exists.

    # For each row in the empty_seats_per_row list
    for (key, val) in empty_seats_per_row.items():
        # If the number of empty seats in the row is equal to the number of
        # passengers plus the constant e, return that True and that row number
        if val == number_of_pas + e: return True, key

    # If no row is found, return False, 0
    return False, 0


def find_allocation_order(number_of_pas, cols, empty_seats_per_row):
    pass


def write_database(engine, command, data):
    pass


def main():
    # Get command line arguments
    filename, db_name = sys.argv[2], sys.argv[1]

    # Read in bookings information
    with open(filename, 'r') as f:
        bookings = [[i.rstrip().split(',')[0], int(i.rstrip().split(',')[1])]
                        for i in f]

    # Create connection engine to database
    engine = create_engine('sqlite:///' + db_name)

    # Retrieve rows and seats information from rows_cols table
    with engine.connect() as con:
        rc = con.execute('SELECT * FROM rows_cols;').fetchall()[0]

    rows, cols = rc[0], rc[1]

    # Set total passengers seated to 0
    passengers_seated = 0

    # For each booking in the list of bookings
    for booking in bookings:
        # Set booking name and number of passengers in booking
        booking_name, pas_in_booking = booking[0], booking[1]

        # If passengers in booking is invalid (negative)
        if pas_in_booking <= 0:
            # Restart the for loop. Do not allocate a seat to the passenger
            print("Invalid booking: %s" % booking_name); continue

        # Retrieve seat map from database, and refresh metrics
        empty_seats, empty_seats_per_row, num_pas_refused, num_pas_split = \
            retrieve_data(engine, rows, cols)

        # If no empty seats available

        # Build the allocation order

        # If the allocation order has splits

        # If allocation order has no splits
        pass


if __name__ == '__main__':
    main()