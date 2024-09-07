import serial
import json
import os
import sys
import time


class SerialPortError(Exception):
    pass


class Raspiduino:

    def __init__(self, serial_port=None, baudrate=1000000):
        # Get the first serial port in the list
        if not serial_port and sys.platform in ["linux", "linux2"]:
            found_ports = os.listdir('/dev/serial/by-path')
            if len(found_ports):
                serial_port = os.path.realpath(os.path.join('/dev/serial/by-path', found_ports[0]))
        
        # Open the chosen port
        try:
            self._ser = serial.Serial(serial_port, baudrate)#, timeout=0.2)
            print("Serial port", serial_port, "succesfully open!")
        except:
            print("Failed to open serial port", serial_port)
            raise SerialPortError
        self._ser.reset_input_buffer()
        self._serial_port = serial_port
        self._baudrate = baudrate
        
    def poll(self):
        read = self._ser.read_until(b'\x03')
        content = json.loads(read[:-1].decode())
        return content
        
    def waitObject(self):
        while True:
            try:
                read = self._ser.read_until(b'\x03')
                # print(read)
                if read and read[-1] == b'\x03'[0]:
                    content = json.loads(read[:-1].decode())
                    return content
            except:
                if self._ser.is_open: self._ser.close()
                self.tryReconnect()
    
    def tryReconnect(self):
        while True:
            try:
                self._ser = serial.Serial(self._serial_port, self._baudrate, timeout=0.01)
                print("Serial port", self._serial_port, "succesfully open!")
                return
            except TimeoutError:
                pass
            except:
                print("Failed to open serial port", self._serial_port)
                raise SerialPortError



if __name__ == '__main__':
    arduino = None
    while not arduino:
        try:
            arduino = Raspiduino()
        except:
            print("Failed to open serial port. Retrying...")
            time.sleep(1)

    while True:
        print(arduino.waitObject())