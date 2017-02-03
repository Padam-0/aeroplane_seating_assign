from nose.tools import *
from sqlalchemy import create_engine
from seat_assign_16201859_16203177 import main, organize_booking, retrieve_data, \
    find_row_with_n_empty_seats, find_allocation_order, write_database


def test_main():
    pass

def test_organize_booking():
    pass

def test_retrieve_data():
    # Inputs
    engine = create_engine('sqlite:///' + "airline_seating.db")
    engine2 = create_engine('sqlite:///' + "test_airline_seating.db")
    rows = 15
    rows2 = 15
    cols = "ACDF"
    cols2 = "ACDF"

    # Outputs - When run on a clean airline_seating.db
    empty_seats = [(1, 'A', ''), (2, 'A', ''), (3, 'A', ''), (4, 'A', ''), (5, 'A', ''),
                   (6, 'A', ''), (7, 'A', ''), (8, 'A', ''), (9, 'A', ''), (10, 'A', ''),
                   (11, 'A', ''), (12, 'A', ''), (13, 'A', ''), (14, 'A', ''), (15, 'A', ''),
                   (1, 'C', ''), (2, 'C', ''), (3, 'C', ''), (4, 'C', ''), (5, 'C', ''),
                   (6, 'C', ''), (7, 'C', ''), (8, 'C', ''), (9, 'C', ''), (10, 'C', ''),
                   (11, 'C', ''), (12, 'C', ''), (13, 'C', ''), (14, 'C', ''), (15, 'C', ''),
                   (1, 'D', ''), (2, 'D', ''), (3, 'D', ''), (4, 'D', ''), (5, 'D', ''),
                   (6, 'D', ''), (7, 'D', ''), (8, 'D', ''), (9, 'D', ''), (10, 'D', ''),
                   (11, 'D', ''), (12, 'D', ''), (13, 'D', ''), (14, 'D', ''), (15, 'D', ''),
                   (1, 'F', ''), (2, 'F', ''), (3, 'F', ''), (4, 'F', ''), (5, 'F', ''),
                   (6, 'F', ''), (7, 'F', ''), (8, 'F', ''), (9, 'F', ''), (10, 'F', ''),
                   (11, 'F', ''), (12, 'F', ''), (13, 'F', ''), (14, 'F', ''), (15, 'F', '')]


    empty_seats_per_row = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4,
                           8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4, 15: 4}
    num_pas_refused = 0
    num_pas_split = 0

    # Outputs - When run on test_airline_seating.db
    empty_seats2 = [(5, 'A', ''), (6, 'A', ''), (7, 'A', ''), (8, 'A', ''), (9, 'A', ''),
                   (10, 'A', ''), (11, 'A', ''), (12, 'A', ''), (13, 'A', ''), (14, 'A', ''),
                   (15, 'A', ''), (4, 'C', ''), (5, 'C', ''), (6, 'C', ''), (7, 'C', ''),
                   (8, 'C', ''), (9, 'C', ''), (10, 'C', ''), (11, 'C', ''), (12, 'C', ''),
                   (13, 'C', ''), (14, 'C', ''), (15, 'C', ''), (4, 'D', ''), (5, 'D', ''),
                   (6, 'D', ''), (7, 'D', ''), (8, 'D', ''), (9, 'D', ''), (10, 'D', ''),
                   (11, 'D', ''), (12, 'D', ''), (13, 'D', ''), (14, 'D', ''), (15, 'D', ''),
                   (4, 'F', ''), (5, 'F', ''), (6, 'F', ''), (7, 'F', ''), (8, 'F', ''),
                   (9, 'F', ''), (10, 'F', ''), (11, 'F', ''), (12, 'F', ''), (13, 'F', ''),
                   (14, 'F', ''), (15, 'F', '')]


    empty_seats_per_row2 = {1: 0, 2: 0, 3: 0, 4: 3, 5: 4, 6: 4, 7: 4,
                           8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4, 15: 4}

    num_pas_refused2 = 0
    num_pas_split2 = 1

    # Unittests
    res1 = retrieve_data(engine, rows, cols)

    assert_equal(res1[0], empty_seats)
    assert_equal(res1[1], empty_seats_per_row)
    assert_equal(res1[2], num_pas_refused)
    assert_equal(res1[3], num_pas_split)

    res2 = retrieve_data(engine2, rows2, cols2)

    assert_equal(res2[0], empty_seats2)
    assert_equal(res2[1], empty_seats_per_row2)
    assert_equal(res2[2], num_pas_refused2)
    assert_equal(res2[3], num_pas_split2)


def test_find_row_with_n_empty_seats():
    pass

def test_find_allocation_order():
    pass

def test_write_database():
    pass

def test_clean_database():
    pass