"""See README.md for module information. """

from sqlalchemy import create_engine, MetaData, Column, Integer, String, \
    Table, VARCHAR
import sys

def clean_database(db_name):
    """Resets a database to have an empty seat chart and zeroed metrics."""

    # Create engine
    engine = create_engine('sqlite:///' + db_name)

    # Set all database fields to empty / 0
    with engine.connect() as con:
        con.execute("UPDATE seating SET name = '';")
        con.execute("UPDATE metrics SET passengers_refused = 0;")
        con.execute("UPDATE metrics SET passengers_separated = 0;")


def create_db(db_name, rows, seats):
    """Creates a test database with a given number of rows and seats"""

    # Create an engine to access the database. Also creates the database if
    # it does not already exist
    engine = create_engine('sqlite:///' + db_name)

    # Load database metadata
    meta = MetaData()

    # Create metrics table
    metrics = Table('metrics', meta,
                      Column('passengers_refused', Integer),
                      Column('passengers_separated', Integer)
                      )
    metrics.create(engine)

    # Create rows_cols table
    rc = Table('rows_cols', meta,
                    Column('nrows', Integer),
                    Column('seats', VARCHAR(16))
                    )
    rc.create(engine)

    # Create seating table
    seating = Table('seating', meta,
                Column('row', Integer, nullable=False),
                Column('seat', VARCHAR(255), nullable=False),
                Column('name', VARCHAR(255)),
               )
    seating.create(engine)

    # Initialise metrics table to 0, rows_cols table to contain informations
    # about number of rows and seat in the plane
    i1 = metrics.insert().values(passengers_refused=0, passengers_separated=0)
    i2 = rc.insert().values(nrows=rows, seats=seats)
    with engine.connect() as con:
        con.execute(i1)
        con.execute(i2)

    # Initialise seating table with all possible combinations of seats
    for j in seats:
        for i in range(1, rows+1):
                i = seating.insert().values(row=i, seat=j, name='')
                with engine.connect() as con:
                    con.execute(i)


def organize_booking(booking_name, pas_in_booking, empty_seats_per_row,
        empty_seats, cols, engine):
    """Allocates seats and writes booking information to the database."""

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


def retrieve_data(engine, rows, cols):
    """Retrieves required seating data from specified database."""

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
    """Find a row which has a number (n) of empty seats if one exists."""

    n = number_of_pas + e

    # For each row in the empty_seats_per_row list
    for (key, val) in empty_seats_per_row.items():
        # If the number of empty seats in the row is equal to the number of
        # passengers plus the constant e, return that True and that row number
        if val == n: return True, key

    # If no row is found, return False, 0
    return False, 0


def find_allocation_order(number_of_pas, cols, empty_seats_per_row):
    """ Sets a list of booking sizes that will be grouped together."""

    # Initialise Allocation Order
    allocation_order = []

    # Create dictionary of number of rows with n empty seats
    rows_with_n_empty_seats = {}
    for n in range(len(cols), 0, -1):
        rows_with_n_empty_seats[n] = \
            len([k for (k, v) in empty_seats_per_row.items() if v == n])

    # Calculate a list of rows with the number of empty seats in rows that
    # have empty seats, ordered from most empty to least empty
    emptiest_rows = []
    for i in range(len(cols), 0, -1):
        if rows_with_n_empty_seats[i] > 0:
            for j in range(rows_with_n_empty_seats[i]): emptiest_rows.append(i)

    # Set booking split to default to True
    split = True

    # Finds if there is a row that has enough empty seats to sit the whole
    # party. If one is found, booking split is set to False
    for i in range(number_of_pas, len(cols) + 1):
        if rows_with_n_empty_seats[i] != 0: split = False; break

    # If booking split is True
    if split:
        # Set the initial leftovers to the booking size
        leftovers = number_of_pas
        remove = True

        # While the whole booking has not been allocated
        while leftovers != 0:
            # If there are more leftovers than the largest number of seats
            # together remaining
            if leftovers > max(emptiest_rows):
                best_row = max(emptiest_rows)
                leftovers -= best_row
            # If there is a row that can fit all leftovers perfectly
            elif leftovers in emptiest_rows:
                best_row = leftovers
                leftovers = 0
            # Otherwise
            else:
                best_row = leftovers
                leftovers = 0
                remove = False

            # Append the number of passengers sitting together
            allocation_order.append(best_row)
            if remove: emptiest_rows.remove(best_row)

    # Else, if Split is False
    else:
        allocation_order = [number_of_pas]


    return allocation_order


def write_database(engine, command, data):
    """Write a SQL command and appropriate data to a given database."""

    with engine.connect() as con:
        con.execute(command, data)


def main():
    # Get command line arguments
    if sys.argv[1] == "clean":
        clean_database(sys.argv[2])
        exit("Database %s Cleaned" % sys.argv[2])
    elif sys.argv[1] == "create":
        create_db(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        exit("Database %s Created" % sys.argv[2])
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
        if pas_in_booking > len(empty_seats):
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
        if len(allocation_order) > 1:
            # Update number of passengers split
            num_pas_split += len(allocation_order) - 1
            write_database(engine, "UPDATE metrics SET "
                        "passengers_separated = ?;", num_pas_split)

            # For each allocation in the allocation order
            for allocation in allocation_order:
                # If there are no empty seats
                if len(empty_seats) <= 0:
                    # Update the number of passengers refused
                    num_pas_refused += allocation
                    # Update metrics table
                    write_database(engine, "UPDATE metrics SET "
                                           "passengers_refused = ?;",
                                   num_pas_refused)

                    print(booking_name, "(" + str(allocation) + ") "
                            "refused."); continue

                # Else, if there are empty seats, allocate Booking and write
                # to the seating table
                organize_booking(booking_name, allocation, empty_seats_per_row,
                    empty_seats, cols, engine)
                passengers_seated += allocation

                # Retrieve seat map from database, and refresh metrics
                empty_seats, empty_seats_per_row, num_pas_refused, \
                    num_pas_split = retrieve_data(engine, rows, cols)

                split = "together"
                if allocation == 1: split = "by self."

                print(booking_name, "(" + str(allocation) + ") seated",
                      split)

        # If allocation order has no splits
        else:
            # Allocate Booking and write to Database
            organize_booking(booking_name, pas_in_booking,
                             empty_seats_per_row, empty_seats, cols, engine)
            passengers_seated += pas_in_booking

            split = "together."
            if pas_in_booking == 1:
                split = "by self."

            print(booking_name, "(" + str(pas_in_booking) + ") seated",
                  split)

    # Print summary information
    print("\n   ---   ***   ---   \n")
    print(passengers_seated, "Passengers Seated")
    print(num_pas_split, "Parties Split")
    print(num_pas_refused, "Refused Entry\n\n")

if __name__ == '__main__':
    main()