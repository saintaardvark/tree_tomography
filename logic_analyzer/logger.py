#!/usr/bin/env python3

import serial
import sys
from time import sleep


BAUDRATE = 921600
HEADER = "chan0,chan1,chan2,chan3,chan4,chan5,chan6,chan7"

START_PIN = 0
NUM_PIN = 8
FREQ = 10_000_000
TRIGGER = 1
SAMPLES = 5000


def set_up(port, baudrate=BAUDRATE, menu=True):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.write(b"\r\n")
    sleep(1)
    if menu:
        # TODO: Use all those constants
        # p0
        ser.write(b"p0\r\n")
        print(ser.readline().decode("utf-8").strip())
        sleep(1)
        # n8
        ser.write(b"n8\r\n")
        print(ser.readline().decode("utf-8").strip())
        sleep(1)
        # f10 000 000
        ser.write(b"f10000000\r\n")
        print(ser.readline().decode("utf-8").strip())
        sleep(1)
        # pt1
        ser.write(b"t1\r\n")
        print(ser.readline().decode("utf-8").strip())
        sleep(1)
        # s5000
        ser.write(b"s5000\r\n")
        print(ser.readline().decode("utf-8").strip())
        sleep(1)
    ser.write(b"g\r\n")
    sleep(1)
    ser.close()


def read_serial_data(port, baudrate=BAUDRATE):
    ser = serial.Serial(port, baudrate, timeout=1)
    data = []

    try:
        while True:
            line = (
                ser.readline().decode("utf-8").strip()
            )  # Read a line from the serial port
            print(line)
            data.append(line)
    except KeyboardInterrupt:
        print("Stopping data collection.")
    finally:
        ser.close()

    return data


# Function to parse the data
def parse_data(data):
    ticks = []
    sensor_states = []

    for line in data:
        parts = line.split(", ")
        tick = int(parts[0].split("=")[1])
        rzf = parts[1].split("=")[1]

        ticks.append(tick)
        sensor_states.append(
            [int(bit) for bit in rzf[::-1]]
        )  # Reverse to match sensor index

    return ticks, np.array(sensor_states)


def fix_line(line: str):
    """Fix line for writing to CSV.

    - remove trailing comma
    - throw away non-csv stuff

    TODO: Fix this in pico firmware.
    """
    if line.endswith(","):
        line = line[:-1]

    if not "," in line:
        print(f"throwing away {line}")
        line = ""

    return line


# Main function
def main():
    # Serial port configuration
    port = "/dev/ttyACM0"  # Change this to your serial port
    print("Setting up...")
    set_up(port, menu=False)

    print("Reading data from serial port...")
    data = read_serial_data(port)

    # print(data)
    with open("foo.csv", "w") as f:
        f.write(f"{HEADER}\n")
        for line in data:
            line = fix_line(line)
            f.write(f"{line}\n")


if __name__ == "__main__":
    main()
