import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns


class DynamicUpdate:
    # TODO: We prob don't know the range
    # Suppose we know the x range
    min_x = 0
    max_x = 10

    def __init__(self):
        self.df = []
        # self.ydata = []
        self.on_launch()

    def update(self, x, y):
        self.xdata.append(x)
        self.ydata.append(y)

    def on_launch(self):
        plt.ion()
        # Set up plot
        self.figure, self.ax = plt.subplots(1, 4)
        # (self.lines,) = self.ax.plot([], [], "o")
        # Autoscale on unknown axis and known lims on the other
        print(len(self.ax))
        for ax in self.ax:
            ax.set_autoscaley_on(True)
            # ax.set_xlim(self.min_x, self.max_x)
            ax.grid()

    def update_graph(self):
        # Update data (with the new _and_ the old points)
        # self.lines.set_xdata(self.xdata)
        # self.lines.set_ydata(self.ydata)
        plt.cla()
        sns.stripplot(data=self.df, ax=self.ax[0])
        sns.scatterplot(data=self.df, ax=self.ax[1], legend=False)
        sns.boxplot(data=self.df, ax=self.ax[2])
        sns.histplot(data=self.df, ax=self.ax[3])
        # Need both of these in order to rescale
        for ax in self.ax:
            ax.relim()
            ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

