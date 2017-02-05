__author__ = "Frantisek Janus"

import usb
# import usb.util
import time
import logging

# TODO AttributeError when starting the script
# TODO usb.core.USBError: [Errno 60] Operation timed out
# TODO How to interupt while loop when running?

class Timy(object):
    """Class responsible for capturing times received from USB device ALGE Timy
    """
    TIMY_VEND = 0x0c4a  # USB Vendor ID
    TIMY_PROD = 0x0889  # USB Product ID
    READEP = 0x81  # Interrupt input endpoint ID
    WRITEEP = 0x01  # Interrupt output endpoint ID

    def __init__(self, timeout=720000, logging=True, logfile="timylog.txt"):
        self.logging = logging
        self.logfile = logfile
        self.timeout = timeout
        self.device_handle = None
        self.kill = False

        if self.logging:
            Timy.logging_init(self.logfile)

        self.find_device()

    def find_device(self):
        # TODO id device not found?
        self.device_handle = usb.core.find(
            idVendor=Timy.TIMY_VEND,
            idProduct=Timy.TIMY_PROD)

        if self.device_handle is None:
            logging.error("ALGE TIMY3 not found. Time capture not possible.")
            return False

        self.device_handle.set_configuration()

    def capture_start(self):
        if self.device_handle is None:
            logging.error("ALGE TIMY3 not found. Time capture not possible.")
            return False

        self.kill = False
        try:
            while True:
                if self.kill:
                    print("stopping the loop")
                    break
                try:
                    time_received = bytearray(self.device_handle.read(
                                        Timy.READEP,
                                        32,
                                        timeout=self.timeout))\
                        .decode("UTF-8").split()

                    if len(time_received) == 4:
                        if time_received[1] == "c1M":
                            print(time_received)
                            logging.debug("Received values: %s - %s - %s - %s", *time_received)
                    time.sleep(0.1)

                except usb.core.USBError as e:
                    if e.args[0] == 60:
                        # To capture usb.core.USBError timeout exception raised after TIMEOUT expires with the code 60
                        # usb.core.USBError: [Errno 60] Operation timed out
                        print("Timeout exception occured.")
                        logging.warning(
                            "Configured timeout %s msec has expired. Recommendation: Increase its value.",
                            self.timeout)
                        pass

                    if e.args[0] == 19:
                        # Device has been disconnected
                        # usb.core.USBError: [Errno 19] No such device (it may have been disconnected)
                        print("Timeout exception occured.")
                        logging.error(
                            "ALGE TIMY USB device has been disconnected",
                            self.timeout)
                        break
                    else:
                        raise e
        finally:
            print("device reset - ending the loop")
            self.device_handle.reset()

    def capture_stop(self):
        if self.device_handle is None:
            logging.error("ALGE TIMY3 not found. Time capture not possible.")
            return False

        self.kill = True

    @staticmethod
    def logging_init(logfile):
        logging.basicConfig(filename=logfile,
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=logging.DEBUG)


def main():
    timy = Timy()
    timy.capture_start()
    timy.capture_stop()


if __name__ == "__main__":
    main()