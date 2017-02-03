from sqlalchemy import create_engine
import sys


def organize_booking(booking_name, pas_in_booking, empty_seats_per_row,
        empty_seats, cols, engine):
    pass


def find_allocation_order(number_of_pas, cols, empty_seats_per_row):
    pass


def write_database(engine, command, data):
    with engine.connect() as con:
        con.execute(command, data)


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