from sqlalchemy import create_engine
import sys

def clean_database(db_name):
    # Create engine
    engine = create_engine('sqlite:///' + db_name)

    # Set all database fields to empty / 0
    with engine.connect() as con:
        con.execute("UPDATE seating SET name = '';")
        con.execute("UPDATE metrics SET passengers_refused = 0;")
        con.execute("UPDATE metrics SET passengers_separated = 0;")


def organize_booking(booking_name, pas_in_booking, empty_seats_per_row,
        empty_seats, cols, engine):
    # Allocates seats and writes to the database for given booking information

    passenger_info = []

    # Find a row with the required number of empty seats
    # Search in empty seats per row list for a match
    for (key,val) in empty_seats_per_row.items():
        # If a perfect match exists, return that row number and exit the loop
        if val == pas_in_booking: row_number = key; break
    # If a perfect row doesn't exist
    else:
        # For each constant e in the range from 1 to the number of seats
        # in each row
        for e in range(1, len(cols)):
            # If a row exists that has more empty seats than required,
            # find_row_with_n_empty_seats returns a list with 2 entries,
            # True and the row number.
            result = find_row_with_n_empty_seats(empty_seats_per_row,
                                                 pas_in_booking, e)
            # If a row exists with more empty seats than required
            if result[0]: row_number = result[1]; break

    # Find seat letters that correspond to empty seats in the required row
    seat_letters = [i[1] for i in empty_seats if i[0] == row_number]

    # Append row and seat information for each passenger in the booking
    for i in range(pas_in_booking):
        passenger_info.append([booking_name, str(row_number),
                               str(seat_letters[i])])

    # Write passenger information to the database
    write_database(engine, "UPDATE seating SET name = ? WHERE row = ? "
                           "AND seat = ?;", passenger_info)


def find_allocation_order(number_of_pas, cols, empty_seats_per_row):
    # Sets the allocation order, a list of allocations that will be grouped
    # together
    allocation_order = []

    # Create dictionary of number of rows with n empty seats
    rows_with_n_empty_seats = {}


    # Calculate a list of rows with the number of empty seats in rows that
    # have empty seats, ordered from most empty to least empty


    # Set Split to default to True
    split = True

    # Finds if there is a row that has enough empty seats to sit the whole
    # party. If one is found, Split is set to False

    # If Split is True
    if split:
        pass

    # Else, if Split is False
    else:
        pass

    return allocation_order


def write_database(engine, command, data):
    with engine.connect() as con:
        con.execute(command, data)


def main():
    # Get command line arguments
    if sys.argv[1] == "clean":
        clean_database(sys.argv[2])
        exit("Database %s Cleaned" % sys.argv[2])
    else:
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
        if len(empty_seats) <= 0:
            #update metric with passengers in booking
            num_pas_refused += pas_in_booking
            write_database(engine, "UPDATE metrics SET "
                "passengers_refused = ?;", num_pas_refused)

            # Return booking name and the number of passengers refused
            print(booking_name, "(" + str(pas_in_booking) + ") "
                    "refused."); continue

        # Build the allocation order
        allocation_order = find_allocation_order(pas_in_booking,
                                                 cols, empty_seats_per_row)

        # If the allocation order has splits

        # If allocation order has no splits
        pass


if __name__ == '__main__':
    main()