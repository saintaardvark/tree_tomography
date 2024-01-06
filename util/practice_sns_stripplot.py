#!/usr/bin/env python3

# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib

from io import StringIO
import sys
import time

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns

from graph.dynamic_update import DynamicUpdate


def main():
    """
    Main entry point
    """
    # Enable pyplot interactive mode:
    plt.ion()
    d = DynamicUpdate()

    while True:
        x = -1
        for line in sys.stdin:
            if x == -1:
                print("save header")
                header = line
                x += 1
                continue
            elif x == 0:
                print("First data line; now make the dataframe")
                first_line = header + line
                d.df = pd.read_csv(StringIO(first_line))
                print(d.df)
                x += 1
                continue
            # Made it here, must not be zeroth or first line
            # df = pd.concat([df, pd.read_csv(StringIO(line), header=0)], ignore_index=True, axis=0)
            d.df = pd.concat(
                [d.df, pd.read_csv(StringIO(line), names=d.df.columns)],
                ignore_index=True,
            )

            # print(line, end="")
            # vals = line.strip(",\n").split(",")
            # print(vals)
            # y = float(line)
            # d.update(x, y)
            x += 1
            if x % 100 == 0:
                d.update_graph()
                print(d.df)


if __name__ == "__main__":
    main()
