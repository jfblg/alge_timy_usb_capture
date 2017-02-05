__author__ = "Frantisek Janus"

# TODO write times to the database
# TODO implement basic commandline interface with infinite loop

from timy import Timy
from database import Time

def main():
    # dev = Timy()
    # dev.capture_start()
    record = Time("fero")
    record.save_to_db()

if __name__ == "__main__":
    main()