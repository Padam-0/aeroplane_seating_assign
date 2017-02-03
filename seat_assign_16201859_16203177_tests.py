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
    engine = create_engine('sqlite:///' + airline_seating)
    rows = None
    cols = None

    # Outputs
    empty_seats = None
    empty_seats_per_row = None
    num_pas_refused = None
    num_pas_split = None



def test_find_row_with_n_empty_seats():
    pass

def test_find_allocation_order():
    pass

def test_write_database():
    pass