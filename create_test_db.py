from sqlalchemy import create_engine, MetaData, Column, Integer, String, \
    Table, VARCHAR, CHAR, PrimaryKeyConstraint
import sys

def create_test_db(db_name, rows, cols):

    engine = create_engine('sqlite:///' + db_name)

    meta = MetaData()

    metrics = Table('metrics', meta,
                      Column('passengers_refused', Integer),
                      Column('passengers_separated', Integer)
                      )
    metrics.create(engine)

    rc = Table('rows_cols', meta,
                    Column('nrows', Integer),
                    Column('seats', VARCHAR(16))
                    )
    rc.create(engine)

    seating = Table('seating', meta,
                Column('row', Integer, nullable=False),
                Column('seat', VARCHAR(255), nullable=False),
                Column('name', VARCHAR(255)),
               )
    seating.create(engine)

    i1 = metrics.insert().values(passengers_refused=0, passengers_separated=0)
    i2 = rc.insert().values(nrows=rows, seats=cols)

    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="A", name='')
            with engine.connect() as con:
                r = con.execute(i)
    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="B", name='')
            with engine.connect() as con:
                r = con.execute(i)
    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="C", name='')
            with engine.connect() as con:
                r = con.execute(i)
    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="D", name='')
            with engine.connect() as con:
                r = con.execute(i)
    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="E", name='')
            with engine.connect() as con:
                r = con.execute(i)
    for i in range(1, rows+1):
            i = seating.insert().values(row=i, seat="F", name='')
            with engine.connect() as con:
                r = con.execute(i)

    with engine.connect() as con:
        r1 = con.execute(i1)
        r2= con.execute(i2)




def main():
    #db_name, rows, cols = sys.argv[1], sys.argv[2], sys.argv[3]
    create_test_db('test2.db', 10, "ABCDEF")

if __name__ == "__main__":
    main()