__author__ = "Frantisek Janus"

import os

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, exc
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_NAME = "db.sqlite"

engine = create_engine("sqlite:///{}".format(os.path.join(os.getcwd(), DB_NAME)))
Session = sessionmaker(bind=engine)


class Time(Base):
    __tablename__ = "time"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Time(id='%s', name='%s')>" % (self.id, self.name)

    def __init__(self, name):
        self.name = name

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
    fero = Time("Fero Janus")
    print(fero)
    fero.save_to_db()
    print("test")

if __name__ == "__main__":
    main()