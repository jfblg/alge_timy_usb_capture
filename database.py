__author__ = "Frantisek Janus"

import os

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, exc
from sqlalchemy import Column, Date, Integer, Interval, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_NAME = "db.sqlite"

engine = create_engine("sqlite:///{}".format(os.path.join(os.getcwd(), DB_NAME)))
Session = sessionmaker(bind=engine)


class TimeModel(Base):
    """Data model definition for SQLAlchemy"""

    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    time_measured = Column(Interval)
    order_number = Column(Integer) # number received from TIMY3 [1-99]

    def __repr__(self):
        return "<Time(id='%s', time_measured='%s', order='%s')>" % (self.id, self.time_measured, self.oder_number)

    def __init__(self, time_measured, order_number):
        self.time_measured = time_measured
        self.order_number = order_number

    def save_to_db(self):
        """Save instance to the database."""
        session = Session()
        try:
            session.add(self)
            session.commit()
        except:
            session().rollback()
            raise
        finally:
            session.close()

Base.metadata.create_all(engine)


def main():
    pass

if __name__ == "__main__":
    main()