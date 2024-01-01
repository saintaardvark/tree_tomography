#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.

from datetime import datetime
import serial
import sys


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

DATA = []


def save(data):
    """
    Save data in some way
    """
    # FIXME: Not really CSV
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    with open(filename, "w") as f:
        f.writelines([f"{i}\n" for i in data])
    print(f"Data file: {filename}")


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(data):
    """
    Graph data in some way
    """
    print(f"Here's a graph!", data)
    # plt.plot(data)
    # plt.show()
    figure, ax = plt.subplots(1, 4)
    # FIXME: axx is a poor variable name
    for axx in ax:
        axx.set_autoscaley_on(True)
        # TODO: See if xlim makes sense here
        # axx.set_xlim(min_x, max_x)
        axx.grid()
    sns.stripplot(data=data, ax=ax[0])
    sns.scatterplot(data=data, ax=ax[1])
    sns.histplot(data=data, ax=ax[3])
    sns.boxplot(data=data, ax=ax[2])
    plt.show()


def log_serial(ser):
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a floating point number

    """
    while True:
        ser_bytes = ser.readline()
        t = float(ser_bytes.decode("utf-8").rstrip("\r\n"))
        print(t)
        DATA.append(t)


def main():
    """
    Main entry point
    """
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200)
    try:
        log_serial(ser)
    except KeyboardInterrupt:
        save(DATA)
        graph(DATA)
        sys.exit()


if __name__ == "__main__":
    main()
