#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.

from datetime import datetime
from io import StringIO
import serial
import sys
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

DATA = []


def save(d, filename):
    """
    Save data in some way

    Args:
      d: DynamicUpdate object
      filename: filename to save, no extension
    """
    # FIXME: Not really CSV
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


class DynamicUpdate:
    def __init__(self):
        self.df = None
        self.on_launch()

    def on_launch(self):
        # Set up plot/
        self.figure, self.ax = plt.subplots(1, 4)
        # (self.lines,) = self.ax.plot([], [], "o")
        # Autoscale on unknown axis and known lims on the other
        print(len(self.ax))
        for ax in self.ax:
            ax.set_autoscaley_on(True)
            # ax.set_xlim(self.min_x, self.max_x)
            ax.grid()

    def update_graph(self):
        print("FIXME: Made it here 1")
        # Update data (with the new _and_ the old points)
        # self.lines.set_xdata(self.xdata)
        # self.lines.set_ydata(self.ydata)
        plt.cla()
        print("FIXME: Made it here 2")

        sns.stripplot(data=self.df, ax=self.ax[0])
        print("FIXME: Made it here 3")

        sns.scatterplot(data=self.df, ax=self.ax[1])
        print("FIXME: Made it here 4")

        sns.boxplot(data=self.df, ax=self.ax[2])
        print("FIXME: Made it here 5")

        sns.histplot(data=self.df, ax=self.ax[3])
        print("FIXME: Made it here 6")

        # Need both of these in order to rescale
        for ax in self.ax:
            print("FIXME: Made it here 7")
            ax.relim()
            print("FIXME: Made it here 8")
            ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        print("FIXME: Made it here 9")

        self.figure.canvas.flush_events()
        print("FIXME: Made it here")


def log_serial(ser, d):
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a CSV line

    Params:
      ser: serial object suitable for reading from
      d: DynamicUpdate object

    """
    x = -1
    header = ""
    print("Waiting for serial...")
    while True:
        ser_bytes = ser.readline()
        line = ser_bytes.decode("utf-8").rstrip("\r\n")
        print(line)
        if x == -1:
            print("save header")
            header = line
            x += 1
            continue
        elif x == 0:
            print("First data line; now make the dataframe")
            first_line = f"{header}\n{line}"
            d.df = pd.read_csv(StringIO(first_line))
            print(d.df)
            x += 1
            continue
        # Made it here, we must have a dataframe already
        d.df = pd.concat(
            [d.df, pd.read_csv(StringIO(line), names=d.df.columns)],
            ignore_index=True,
        )
        print(f"[FIXME] {len(d.df)=}")
        print(f"[FIXME] {(len(d.df) % 10)=}")
        if len(d.df) % 10 == 0:
            print("Updating graph!")
            d.update_graph()


def main():
    """
    Main entry point
    """
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200)
    ser.send_break()
    ser.write(b"\x04")  # send ^D (EOT)
    # sleep(0.1)
    d = DynamicUpdate()
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    try:
        plt.ion()
        log_serial(ser, d)
    except KeyboardInterrupt:
        save(d, filename)
        graph(d, filename)
        sys.exit()


if __name__ == "__main__":
    main()
