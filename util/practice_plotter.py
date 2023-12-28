#!/usr/bin/env python3

# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib

import sys
import time

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


class DynamicUpdate:
    # Suppose we know the x range
    min_x = 0
    max_x = 10

    def __init__(self):
        self.on_launch()
        self.xdata = []
        self.ydata = []

    def update(self, x, y):
        self.xdata.append(x)
        self.ydata.append(y)
        self.on_running()

    def on_launch(self):
        # Set up plot
        self.figure, self.ax = plt.subplots()
        (self.lines,) = self.ax.plot([], [], "o")
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        # Other stuff
        self.ax.grid()

    def on_running(self):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(self.xdata)
        self.lines.set_ydata(self.ydata)
        # Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    # Example
    def __call__(self):
        for x in np.arange(0, 10, 0.5):
            xdata.append(x)
            ydata.append(np.exp(-(x**2)) + 10 * np.exp(-((x - 7) ** 2)))
            self.on_running(xdata, ydata)
            time.sleep(1)
        return xdata, ydata


def main():
    """
    Main entry point
    """
    plt.ion()
    d = DynamicUpdate()

    while True:
        x = 0
        for line in sys.stdin:
            print(line, end="")
            y = float(line)
            d.update(x, y)
            x += 1


if __name__ == "__main__":
    main()
