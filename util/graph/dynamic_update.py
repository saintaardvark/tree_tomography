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

    def filter_data(
        self, filter_zeroes: bool = True, filter_outliers: bool = True
    ) -> pd.DataFrame:
        """
        Filter self.df, and return a copy of that dataframe.

        Args:

          filter_zeroes (bool): if True, filter out any row that has a zero in it.
          filter_outliers (bool): if True, filter out any outliers.

        Returns

        The current implementation filters outliers by looking for data outside the Interquartile distance.
        From https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-a-pandas-dataframe/69001342#69001342:

        Even more robust version of the quantile principle: Eliminate
        all data that is more than f times the interquartile range away
        from the median of the data. That's also the transformation that
        sklearn's RobustScaler uses for example. IQR and median are robust
        to outliers, so you outsmart the problems of the z-score approach.

        In a normal distribution, we have roughly iqr=1.35*s, so you
        would translate z=3 of a z-score filter to f=2.22 of an
        iqr-filter. This will drop the 999 in the above example.

        The basic assumption is that at least the "middle half" of
        your data is valid and resembles the distribution well,
        whereas you also mess up if your distribution has wide tails
        and a narrow q_25% to q_75% interval.

        """
        df = self.df.copy()
        if filter_zeroes:
            df = df.replace(0, np.nan)
            df = df.dropna(how="any", axis=0)

        if filter_outliers:
            # OPTION 3: iqr filter: within 2.22 IQR (equiv. to z-score < 3)
            cols = df.select_dtypes(
                "number"
            ).columns  # limits to a (float), b (int) and e (timedelta)
            iqr = df.quantile(0.75, numeric_only=False) - df.quantile(
                0.25, numeric_only=False
            )
            lim = np.abs((df - df.median()) / iqr) < 2.22
            # replace outliers with nan
            df.loc[:, cols] = df.where(lim, np.nan)

        return df

    def update_graph(self, filter_data: bool = True):
        """
        Update graph.

        Args:
          filter_data (bool): if true, filter the data with self.filter_data().
        """
        # Update data (with the new _and_ the old points)
        # self.lines.set_xdata(self.xdata)
        # self.lines.set_ydata(self.ydata)
        plt.cla()
        df = self.df
        if filter_data:
            df = self.filter_data()
        sns.stripplot(data=df, ax=self.ax[0])
        sns.scatterplot(data=df, ax=self.ax[1], legend=False)
        sns.boxplot(data=df, ax=self.ax[2])
        sns.histplot(data=df, ax=self.ax[3])
        # Need both of these in order to rescale
        for ax in self.ax:
            ax.relim()
            ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
