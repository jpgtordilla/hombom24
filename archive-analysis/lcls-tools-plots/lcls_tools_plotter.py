import sys

sys.path.append(
    '/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools')  # change to your path
# to lcls_tools
import common.data_analysis.archiver as arch  # type: ignore
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import find_peaks


class LclsToolsPlotter:
    def __init__(self):
        self.charge_vals = []  # TODO: FILL WITH CHARGE VALUES
        return

    """GENERAL PLOTS"""

    def create_df(self, pv_str: str, start: str, end: str) -> pd.DataFrame:
        """Create and return a DataFrame given a PV and start/end date.

        Keyword arguments:
        pv_str -- The PV to plot
        start -- The start date of the plot in YYYY/MM/DD HH:MM:SS format
        end -- The end date of the plot in YYYY/MM/DD HH:MM:SS format
        """
        # specify a start and end date
        format_string = "%Y/%m/%d %H:%M:%S"
        start_date_obj = datetime.strptime(start, format_string)  # create a datetime object
        end_date_obj = datetime.strptime(end, format_string)
        # submit request with a list of PVs
        data = arch.get_values_over_time_range([pv_str], start_date_obj, end_date_obj)
        # create a dictionary for a PV, access it with timestamps and values methods from archiver.py
        pv_dict = data[pv_str]
        pv_timestamps = pv_dict.timestamps
        pv_values = pv_dict.values
        pv_clean_timestamps = [pv_timestamps[i].strftime('%m/%d/%Y %H:%M:%S') for i in
                               range(len(pv_timestamps))]  # clean and reformat timestamps from the dict
        return pd.DataFrame({"timestamps": pv_clean_timestamps, pv_str: pv_values})  # create df with columns

    def plot_pv_over_time(self, pv_list: list[str], start: str, end: str):
        """Plots a nonempty list of PVs over time.

        Keyword arguments:
        pv_list -- A list of PVs to plot
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        """
        fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
        if len(pv_list) > 0:
            for pv_str in pv_list:
                df = self.create_df(pv_str, start, end)
                ax.scatter(df["timestamps"], df[pv_str], label=pv_str)
                ax.set_xlabel("Timestamp")
            ax.xaxis.set_major_locator(ticker.LinearLocator(5))
            ax.set_title("PVs vs. Time")
            ax.legend()
            plt.show()
        else:
            return "Could not plot PVs because an empty list was given"

    def megaplot_pvs_over_time(self, pv_list: list[str], start: str, end: str, w_margin=0.4, h_margin=1):
        """Create a megaplot of PVs with respect to time.

        Keyword arguments:
        pv_list -- A list of PVs to plot
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        """
        if len(pv_list) < 1:
            return IndexError("Could not plot PVs because an empty list was given")
        # if the length of pv_list is only 1, call the single plot function 
        if len(pv_list) == 1:
            self.plot_pv_over_time([pv_list[0]], start, end)
            return
        # want to create a grid of subplots
        col_len = len(pv_list)
        dim = int(np.round(np.sqrt(col_len)))  # dimension of the grid

        # IF DIMENSION < 2: create two subplots side by side
        if dim < 2:
            fig, (ax0, ax1) = plt.subplots(1, 2)
            fig.suptitle("PVs vs. Time")
            # generate dfs and axes for each pv
            for i in range(2):
                pv_str = pv_list[i]
                curr_ax = fig.get_axes()[i]
                df = self.create_df(pv_str, start, end)
                curr_ax.scatter(df["timestamps"], df[pv_str], label=pv_str)
                curr_ax.set_xlabel("Timestamp", fontsize=10)
                curr_ax.xaxis.set_major_locator(ticker.LinearLocator(3))
                curr_ax.set_xticklabels(df["timestamps"], fontsize=5)
                # y tick scientific notation
                curr_ax.yaxis.set_major_locator(ticker.LinearLocator(5))
                y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[pv_str]]
                curr_ax.set_yticklabels(y_ticks, fontsize=5)
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin)

        # IF DIMENSION >= 2: create a grid of subplots that are indexed in a loop 
        else:
            fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))  # add an extra row to account for rounding
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin)  # can set if needed using optional parameters
            df_ind = 0  # track index of the which df is being plotted

            # create a list of DataFrames for each pv in pv_list
            df_list = [self.create_df(pv_list[i], start, end) for i in range(len(pv_list))]

            # iterate through the grid 
            for i in range(0, dim + 1):  # for every row in the grid
                for j in range(0, dim):  # for every column in the grid
                    if df_ind >= len(df_list):
                        break
                    self.plot_mega(ax, df_list[df_ind], i, j)
                    df_ind += 1  # go to the next df in the list
        plt.show()
        return

    @staticmethod
    def plot_mega(ax: plt.axes, df: pd.DataFrame, i: int, j: int):
        """Grid plotter helper function for megaplots. Called for each DataFrame and Axis in the grid.

        Keyword arguments:
        ax -- The axes to plot
        df -- The current dataframe to plot
        i -- The index of the row to plot
        j -- The index of the column to plot
        """
        ax[i, j].scatter(df["timestamps"], df[df.columns[1]], s=10)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].set_xlabel("Timestamp")
        # y tick scientific notation
        y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[df.columns[1]]]
        ax[i, j].set_yticklabels(y_ticks, fontsize=5)
        ax[i, j].yaxis.set_major_locator(ticker.LinearLocator(5))
        ax[i, j].set_title(f"PV vs. Time for {df.columns[1]}", {'fontsize': 10})
        return

    """PEAK FILTERING"""

    @staticmethod
    def create_peaks_df(df_curr: any, pv_name: str, peak_indices: list[int], peak_heights: list[float]) -> pd.DataFrame:
        """Helper method to return a DataFrame of peaks over time given lists for peak indices and peak heights.

        Keyword arguments:
        df_curr -- The current dataframe to plot
        pv_name -- The name of the PV to plot
        peak_indices -- A list of indices of the peaks to plot
        peak_heights -- A list of heights of the peaks to plot
        """
        all_timestamps_list = df_curr["timestamps"].tolist()
        peak_timestamps_list = [all_timestamps_list[x] for x in peak_indices]
        peak_df_data = {"timestamps": peak_timestamps_list, pv_name: peak_heights}
        peak_df = pd.DataFrame(data=peak_df_data, index=[x for x in range(len("timestamps"))])
        return peak_df

    def return_peaks(self, pv_list: list[str], start: str, end: str, peak_height: float, peak_spacing: float) \
            -> IndexError | list[pd.DataFrame]:
        """Return a List of DataFrames over time of timestamps/peaks given a list of PVs.

        Keyword arguments:
        pv_list -- A list of PVs to plot
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        peak_height -- The minimum height of peaks to plot
        peak_spacing -- The spacing of data points between the peaks to plot
        """
        if len(pv_list) < 1:
            return IndexError("Could not plot PVs because an empty list was given")
        peak_df_list = []  # list of DataFrames containing peak data
        for pv_name in pv_list:
            df_curr = self.create_df(pv_name, start, end)
            y_axis = df_curr[pv_name]  # get the column that corresponds with the pv values
            peak_indices, peak_heights = find_peaks(y_axis, height=peak_height,
                                                    distance=peak_spacing)  # use scipy to generate lists of peak
            # indices and their heights
            peak_indices_2, peak_heights_2 = find_peaks(-y_axis, height=peak_height,
                                                        distance=peak_spacing)  # find minima
            # combine lists of maxima and minima
            all_peak_indices = np.concatenate((peak_indices, peak_indices_2), axis=None)
            all_peak_heights = np.concatenate((peak_heights["peak_heights"], peak_heights_2["peak_heights"]), axis=None)
            # return a DataFrame with timestamps and peaks
            peak_df = self.create_peaks_df(df_curr, pv_name, all_peak_indices.tolist(), all_peak_heights.tolist())
            peak_df_list.append(peak_df)

        return peak_df_list

    def plot_return_peaks(self, pv_list: list[str], start: str, end: str, peak_height: float, peak_spacing: float,
                          is_correl=False) -> list[pd.DataFrame]:
        """Plot peaks on a PV graph as well as the individual data points and return the 2D dictionary.

        Keyword arguments:
        pv_list -- A list of PVs to plot
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        peak_height -- The minimum height of peaks to plot
        peak_spacing -- The spacing of data points between the peaks to plot
        is_correl -- whether to plot the correlation between the second item in the list vs. the first item: [x, y]
        """
        # plot peaks based on parameters
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        plt.subplots_adjust(wspace=0.4, hspace=0.3)

        # IF PLOTTING A CORRELATION
        if is_correl:
            df_curr = self.create_correlation_df(pv_list[0], pv_list[1], start, end)
            y = df_curr[pv_list[1]]
            x = df_curr[pv_list[0]]
            all_peaks, peak_heights = find_peaks(y, height=peak_height,
                                                 distance=peak_spacing)  # use scipy to generate lists of peak
            # indices and their heights
            ax[0].scatter(df_curr[pv_list[0]], df_curr[pv_list[1]])

            # plot only peak points with x-axis showing index corresponding to the returned dict
            ax[1].scatter(all_peaks, y[all_peaks])
            # match limits (approximately) with the first plot
            ax[1].set_xlim(0, len(x))

            # set labels
            for i in range(2):
                ax[i].set_xlabel(f"{pv_list[0]}")
                ax[i].set_ylabel(f"{pv_list[1]}")
                ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
                ax[i].yaxis.set_major_locator(ticker.LinearLocator(5))
                # set significant figures
                x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                           x]  # convert to scientific notation
                y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in y]
                ax[i].set_xticklabels(x_ticks, fontsize=10)  # set tick labels
                ax[i].set_yticklabels(y_ticks, fontsize=10)  # set tick labels
                ax[i].set_title(f"{pv_list[1]} vs. {pv_list[0]}")

        # IF PLOTTING A TIMESERIES
        else:
            for pv_name in pv_list:
                df_curr = self.create_df(pv_name, start, end)
                y = df_curr[pv_name]
                all_peaks, peak_heights = find_peaks(y, height=peak_height,
                                                     distance=peak_spacing)  # use scipy to generate lists of peak
                # indices and their heights
                ax[0].scatter(df_curr["timestamps"], y)
                ax[0].plot(all_peaks, y[all_peaks], "x", color="red")
                ax[0].plot(np.zeros_like(y), "--", color="gray")
                # plot only peak points with x-axis showing index corresponding to the returned dict
                ax[1].scatter(all_peaks, y[all_peaks])
                # match limits (approximately) with the first plot
                ax[1].set_xlim(0, len(df_curr["timestamps"]))
            ax[0].legend()

            # set labels
            for i in range(2):
                ax[i].set_xlabel("Timestamp")
                ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
                ax[i].set_xticklabels(df_curr["timestamps"], fontsize=10)  # set tick labels
                ax[i].set_title(f"PV vs. Time")

        plt.show()
        return self.return_peaks(pv_list, start, end, peak_height, peak_spacing)

    def return_peaks_from_df(self, df: pd.DataFrame, peak_height: float, peak_spacing: float) -> list[pd.DataFrame]:
        """Returns list of DataFrames with timestamps/peaks from a correlation DataFrame.

        Keyword arguments:
        df -- The DataFrame to plot
        peak_height -- The minimum height of peaks to plot
        peak_spacing -- The spacing of data points between the peaks to plot
        """
        peak_df_list = []
        for pv_name in df.columns:
            if pv_name == "timestamps":
                continue
            y_axis = df[pv_name]  # get the column that corresponds with the pv values
            peak_indices, peak_heights = find_peaks(y_axis, height=peak_height,
                                                    distance=peak_spacing)  # use scipy to generate lists of peak
            # indices and their heights
            peak_indices_2, peak_heights_2 = find_peaks(-y_axis, height=peak_height,
                                                        distance=peak_spacing)  # find minima
            # combine lists of maxima and minima
            all_peak_indices = np.concatenate((peak_indices, peak_indices_2), axis=None)
            all_peak_heights = np.concatenate((peak_heights["peak_heights"], peak_heights_2["peak_heights"]), axis=None)
            # return a DataFrame with timestamps and peaks
            peak_df = self.create_peaks_df(df, pv_name, all_peak_indices.tolist(), all_peak_heights.tolist())
            peak_df_list.append(peak_df)
        return peak_df_list

    def plot_peaks_from_df(self, df: pd.DataFrame, pv_y: str, pv_x: str, peak_height: float, peak_spacing: float,
                           show_plots=True) -> list[pd.DataFrame]:
        """Plot peaks from a DataFrame.

        Keyword arguments:
        df -- The DataFrame to plot
        pv_y -- The name of the PV that will be plotted on the y-axis
        pv_x -- The name of the PV that will be plotted on the x-axis
        peak_height -- The minimum height of peaks to plot
        peak_spacing -- The spacing of data points between the peaks to plot
        show_plots -- Whether to show the plot in a window or not.
        """
        # plot peaks based on parameters
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        plt.subplots_adjust(wspace=0.4, hspace=0.3)
        y = df[pv_y]
        x = df[pv_x]
        all_peaks, peak_heights = find_peaks(y, height=peak_height,
                                             distance=peak_spacing)  # use scipy to generate lists of peak indices
        # and their heights
        ax[0].scatter(df[pv_x], df[pv_y])
        # plot only peak points with x-axis showing index corresponding to the returned dict
        ax[1].scatter(all_peaks, y[all_peaks])
        # match limits (approximately) with the first plot
        ax[1].set_xlim(0, len(x))
        # set labels
        for i in range(2):
            ax[i].set_xlabel(f"{pv_x}")
            ax[i].set_ylabel(f"{pv_y}")
            ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
            ax[i].yaxis.set_major_locator(ticker.LinearLocator(5))
            # set significant figures
            x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                       x]  # convert to scientific notation
            y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in y]
            ax[i].set_xticklabels(x_ticks, fontsize=10)  # set tick labels
            ax[i].set_yticklabels(y_ticks, fontsize=10)  # set tick labels
            ax[i].set_title(f"{pv_y} vs. {pv_x}")

        if show_plots:
            plt.show()

        return self.return_peaks_from_df(df, peak_height, peak_spacing)

    """CORRELATIONS"""

    def create_correlation_df(self, pv_one: pd.DataFrame | str, pv_two: str, start: str, end: str) -> pd.DataFrame:
        """Given two PVs, return a single DataFrame with matching and aligned timestamps.

        Keyword arguments:
        pv_one -- The name of the PV or the DataFrame that will be plotted on the y-axis
        pv_two -- The name of the PV that will be plotted on the x-axis
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        """
        df_one = None
        if type(pv_one).isinstance(pd.DataFrame):
            df_one = pv_one
        else:
            df_one = self.create_df(pv_one, start, end)
        df_two = self.create_df(pv_two, start, end)
        return pd.merge(df_one, df_two, on="timestamps")  # merge DataFrames on equal timestamp strings

    def create_correlation_charge_df(self, pv_charge: str, pv_one: str, pv_two: str, start: str, end: str,
                                     charge: float, tolerance: float) -> pd.DataFrame:
        """Given three PVs, return a single DataFrame with matching and aligned timestamps, by a specific charge.

        Keyword arguments:
        pv_one -- The name of the PV or the DataFrame that will be plotted on the y-axis
        pv_two -- The name of the PV that will be plotted on the x-axis
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        charge -- The charge of the PV in pC
        tolerance -- the percent deviation between clusters of different charges (between 0 and 1)
        """
        # align all three PVs with each other by timestamp
        df_charge_pv_one = self.create_correlation_df(pv_charge, pv_one, start, end)
        df_all_correl = self.create_correlation_df(df_charge_pv_one, pv_two, start, end)
        # eliminate rows with charge values outside the tolerance percentage
        df_filtered = df_all_correl[(df_all_correl[pv_charge] > (charge - (tolerance * charge))) & (
                df_all_correl[pv_charge] < (charge + (tolerance * charge)))]
        return df_filtered

    # TODO: FILL WITH CHARGE VALUES
    def plot_correlation(self, pv_list: list[str], start: str, end: str, charge=20, tolerance=0.05):
        """Plot the correlation of the first two PVs in pv_list, potentially separated by charge

        Keyword arguments:
        pv_list -- The list of PVs that will be plotted on the y-axis. If more than 2 PVs, 1-2 plotted and 3 is charge
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        charge -- The charge of the PV in pC
        tolerance -- the percent deviation between clusters of different charges (between 0 and 1)
        """
        fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
        # define what PVs will be plotted and use conditionals to determine whether to separate by charge
        pv_one = pv_list[0]
        pv_two = pv_list[1]
        df = None
        if len(pv_list) > 2:  # if there is a charge PV, filter out unwanted values
            pv_charge = pv_list[2]
            df = self.create_correlation_charge_df(pv_charge, pv_one, pv_two, start, end, charge, tolerance)
        else:
            df = self.create_correlation_df(pv_one, pv_two, start, end)
        ax.scatter(df[pv_one], df[pv_two], label=f"{pv_two} vs. {pv_one}")
        # tick settings
        x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                   df[pv_one]]  # convert to scientific notation
        y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[pv_two]]
        ax.set_xticklabels(x_ticks, fontsize=10)  # set tick labels
        ax.set_yticklabels(y_ticks, fontsize=10)
        ax.xaxis.set_major_locator(ticker.LinearLocator(5))
        ax.yaxis.set_major_locator(ticker.LinearLocator(5))
        # plot labels
        ax.set_xlabel(f"{pv_one}")
        ax.set_ylabel(f"{pv_two}")
        ax.set_title(f"{pv_two} vs. {pv_one}")
        ax.legend()
        plt.show()
        return

    def megaplot_correlation(self, pv_y: str, pv_list: list[str], start: str, end: str, w_margin=0.4, h_margin=1):
        """Megaplot of correlation between a PV vs. a list of PVs.

        Keyword arguments:
        pv_y -- The name of the PV or the DataFrame that will be plotted on the y-axis
        pv_list -- The list of PVs that will be plotted on the x-axis
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        w_margin -- horizontal space between subplots
        h_margin -- vertical space between subplots
        """
        if len(pv_list) < 1:
            return IndexError("Could not plot PVs because an empty list was given")
        # if the length of pv_list is only 1, call the non-megaplot correlation function 
        if len(pv_list) == 1:
            self.plot_correlation([pv_list[0], pv_y], start, end)
            return
        # want to create a grid of subplots
        col_len = len(pv_list)
        dim = int(np.round(np.sqrt(col_len)))  # dimension of the grid

        # IF DIMENSION < 2: create two subplots side by side
        if dim < 2:
            fig, (ax0, ax1) = plt.subplots(1, 2)
            fig.suptitle("PV Correlations")
            # generate dfs and axes for each pv
            for i in range(2):
                curr_ax = fig.get_axes()[i]
                curr_pv_x = pv_list[i]  # the current pv in the pv_list
                df = self.create_correlation_df(pv_y, curr_pv_x, start, end)  # create single df with aligned timestamps
                curr_ax.scatter(df[curr_pv_x], df[pv_y], label=curr_pv_x)
                # tick settings
                x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                           df[curr_pv_x]]  # convert to scientific notation
                y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[pv_y]]
                curr_ax.set_xticklabels(x_ticks, fontsize=5)
                curr_ax.set_yticklabels(y_ticks, fontsize=5)
                curr_ax.xaxis.set_major_locator(ticker.LinearLocator(5))
                curr_ax.yaxis.set_major_locator(ticker.LinearLocator(5))
                # set labels
                curr_ax.set_xlabel(f"{curr_pv_x}", fontsize=10)
                curr_ax.set_ylabel(f"{pv_y}", fontsize=10)
                curr_ax.set_title(f"{pv_y} vs. {curr_pv_x}", fontsize=5)
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin)

        # IF DIMENSION >= 2: create a grid of subplots that are indexed in a loop 
        else:
            fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))  # add an extra row to account for rounding
            fig.suptitle("PV Correlations")
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin)  # can set if needed using optional parameters
            pv_ind = 0  # track index of the which pv is being plotted

            # iterate through the grid 
            for i in range(0, dim + 1):  # for every row in the grid
                for j in range(0, dim):  # for every column in the grid
                    if pv_ind >= len(pv_list):
                        break
                    self.plot_correl_mega(ax, pv_y, i, j, pv_list, pv_ind, start, end)
                    pv_ind += 1  # go to the next df in the list
        plt.show()
        return

    def plot_correl_mega(self, ax: any, pv_y: str, i: int, j: int, pv_list: list[str], pv_ind: int, start: str, end: str):
        """Grid plotter helper function for megaplots. Called for each PV and Axis in the grid.

        Keyword arguments:
        ax -- The matplotlib axis to be plotted
        pv_y -- The name of the PV that will be plotted on the y-axis
        i -- The index of the row that will be plotted
        j -- the index of the column that will be plotted
        pv_list -- The list of PVs that will be plotted on the x-axis
        pv_ind -- The index of the PV that will be plotted on the x-axis
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        """
        x_col = pv_list[pv_ind]
        y_col = pv_y
        df = self.create_correlation_df(pv_list[pv_ind], pv_y, start, end)
        ax[i, j].scatter(df[x_col], df[y_col], s=10)
        # tick settings
        x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                   df[x_col]]  # convert to scientific notation
        y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[y_col]]
        ax[i, j].set_xticklabels(x_ticks, fontsize=5)
        ax[i, j].set_yticklabels(y_ticks, fontsize=5)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(5))
        ax[i, j].yaxis.set_major_locator(ticker.LinearLocator(5))
        # set labels
        ax[i, j].set_xlabel(f"{x_col}")
        ax[i, j].set_ylabel(f"{y_col}")
        ax[i, j].set_title(f"{y_col} vs. {x_col}", {'fontsize': 10})
        return

    def megaplot_correlation_charge_separated(self, pv_x: str, pv_y: str, pv_charge: str, start: str, end: str,
                                              tolerance=0.05, w_margin=0.4, h_margin=1):
        """Megaplotter that creates a correlation between two PVs with respect to a charge PV, for each charge value.

        Keyword arguments:
        pv_x -- The name of the PV that will be plotted on the x-axis
        pv_y -- The name of the PV that will be plotted on the y-axis
        pv_charge -- The name of the PV containing charge values that will be on separate subplots
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        tolerance -- The margin between the x-axis and the y-axis (in percent)
        w_margin -- horizontal space between subplots
        h_margin -- vertical space between subplots
        """
        # want to create a grid of subplots
        col_len = len(self.charge_vals)
        dim = int(np.round(np.sqrt(col_len)))  # dimension of the grid

        fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))  # add an extra row to account for rounding
        fig.suptitle("PV Correlations")
        plt.subplots_adjust(wspace=w_margin, hspace=h_margin)  # can set if needed using optional parameters
        charge_ind = 0  # track index of the which pv is being plotted

        # iterate through the grid 
        for i in range(0, dim + 1):  # for every row in the grid
            for j in range(0, dim):  # for every column in the grid
                if charge_ind >= len(self.charge_vals):
                    break
                self.plot_correl_charge_mega(ax, pv_x, pv_y, pv_charge, i, j, charge_ind, start, end, tolerance)
                charge_ind += 1  # go to the next df in the list
        plt.show()
        return

    def plot_correl_charge_mega(self, ax: plt.axes, pv_x: str, pv_y: str, pv_charge: str, i: int, j: int,
                                charge_ind: int, start: str, end: str, tolerance: float):
        """Helper method for megaplotter between two PVs with respect to charge. Called for each Axis in the grid.

        Keyword arguments:
        ax -- The matplotlib axis to be plotted
        pv_x -- The name of the PV that will be plotted on the x-axis
        pv_y -- The name of the PV that will be plotted on the y-axis
        pv_charge -- The name of the PV containing charge values that will be on separate subplots
        i -- The index of the row that will be plotted
        j -- The index of the column that will be plotted
        charge_ind -- The index of the charge that will be on separate subplots
        start -- The start date of the plot in YYYY/MM HH:MM:SS format
        end -- The end date of the plot in YYYY/MM HH:MM:SS format
        tolerance -- the percent deviation between clusters of different charges (between 0 and 1)
        """
        x_col = pv_x
        y_col = pv_y
        charge = self.charge_vals[charge_ind]
        df = self.create_correlation_charge_df(pv_charge, pv_x, pv_y, start, end, charge,
                                               tolerance)  # create correlation between pv_x and pv_y for each charge
        ax[i, j].scatter(df[x_col], df[y_col], s=10)
        # tick settings
        x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in
                   df[x_col]]  # convert to scientific notation
        y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[y_col]]
        ax[i, j].set_xticklabels(x_ticks, fontsize=5)
        ax[i, j].set_yticklabels(y_ticks, fontsize=5)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(5))
        ax[i, j].yaxis.set_major_locator(ticker.LinearLocator(5))
        # set labels
        ax[i, j].set_xlabel(f"{x_col}")
        ax[i, j].set_ylabel(f"{y_col}")
        ax[i, j].set_title(f"{y_col} vs. {x_col}", {'fontsize': 10})
        return
