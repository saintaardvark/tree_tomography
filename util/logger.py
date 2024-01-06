#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.

from datetime import datetime
from io import StringIO
import pathlib
import serial
import sys
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

filepath = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(filepath / "../micropython/constants"))

from headers import DEFAULT_HEADERS

from graph.dynamic_update import DynamicUpdate


def save(d, filename):
    """
    Save data in some way

    Args:
      d: DynamicUpdate object
      filename: filename to save, no extension
    """
    d.df.to_csv(f"{filename}.csv")
    print(f"Data file: {filename}.csv")


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(d, filename):
    """
    Graph data in some way

    Args;
      d: DynamicUpdate object
      filename: filename for figure, no extension
    """
    print(f"Here's a graph!")
    # plt.plot(data)
    # plt.show()
    figure, ax = plt.subplots(1, 4)
    # FIXME: axx is a poor variable name
    for axx in ax:
        axx.set_autoscaley_on(True)
        # TODO: See if xlim makes sense here
        # axx.set_xlim(min_x, max_x)
        axx.grid()
    sns.stripplot(data=d.df, ax=ax[0])
    sns.scatterplot(data=d.df, ax=ax[1], legend=False)
    sns.histplot(data=d.df, ax=ax[3])
    sns.boxplot(data=d.df, ax=ax[2])
    plt.savefig(f"{filename}.png")
    plt.show()


def log_serial(ser, d, headers=DEFAULT_HEADERS):
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a CSV line

    Params:
      ser: serial object suitable for reading from
      d: DynamicUpdate object
      default_headers: default headers for the CSV values
    """
    x = 0
    print("Waiting for serial...")
    while True:
        ser.send_break()
        ser.write(b"\x04")  # send ^D (EOT)
        ser_bytes = ser.readline()
        line = ser_bytes.decode("utf-8").rstrip("\r\n")
        print(line)
        if x == 0:
            print("First data line; now make the dataframe")
            first_line = f"{headers}\n{line}"
            d.df = pd.read_csv(StringIO(first_line))
            x += 1
            continue
        # Made it here, we must have a dataframe already
        d.df = pd.concat(
            [d.df, pd.read_csv(StringIO(line), names=d.df.columns)],
            ignore_index=True,
        )
        if len(d.df) % 10 == 0:
            print("Updating graph!")
            d.update_graph()


def main():
    """
    Main entry point
    """
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200)
    # sleep(0.1)
    d = DynamicUpdate()
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    try:
        log_serial(ser, d)
    except KeyboardInterrupt:
        save(d, filename)
        graph(d, filename)
        sys.exit()


if __name__ == "__main__":
    main()
