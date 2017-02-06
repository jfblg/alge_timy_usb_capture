__author__ = "Frantisek Janus"

# TODO write times to the database
# TODO implement basic commandline interface with infinite loop

from timy import Timy

def main():
    dev = Timy()
    dev.capture_start()

if __name__ == "__main__":
    main()