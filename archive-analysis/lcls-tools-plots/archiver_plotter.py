import sys
sys.path.append('/archive-analysis/lcls-tools-plots/lcls_tools')  # TODO: change to your path to lcls_tools
import common.data_analysis.archiver as arch  # type: ignore
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class ArchiverPlotter:
    def __init__(self):
        return

    def create_df(self, pv_str: str, start: str, end: str) -> pd.DataFrame:
        """Create and return a DataFrame given a PV and start/end date.

        Column titles of the DataFrame are "timestamps" and the pv_str. 

        :param pv_str: The PV to plot.
        :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format.
        :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format.
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
    
    def create_correlation_df(self, df_x: pd.DataFrame, df_y: pd.DataFrame) -> pd.DataFrame:
        """Given two DataFrames of PVs, return a single DataFrame with matching and aligned timestamps.

        :param df_y: The name of the PV or the DataFrame that will be plotted on the y-axis.
        :param df_x: The name of the PV that will be plotted on the x-axis.
        """
        
        return pd.merge(df_y, df_x, on="timestamps")  # merge DataFrames on equal timestamp strings

    def plot_pv_over_time(self, df_list: list[pd.DataFrame], start: str, end: str) -> None:
        """Plots a nonempty list of PVs over time.

        :param df_list: A list of DataFrames from which to plot the PVs. 
        :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format.
        :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format.
        """

        # TODO: 
        # - width/height
        # - xlabel bottom, top
        # - ylabel left, right
        # - xlabel_color bottom, top
        # - ylabel_color left, right
        # - xlabel_font bottom, top
        # - ylabel_font left, right
        # - xlabel_fontsize bottom, top
        # - ylabel_fontsize left, right
        # - linecolors list
        # - linetypes list
        # - label list 
        # - datetime, algorithm to check what is changing, but changing the least (days, minutes, seconds, etc.)

        ax = plt.subplots(figsize=(10, 7), layout='constrained') 
        for i in range(len(df_list)): 
            df_curr = df_list[i]
            ax.scatter(df_curr["timestamps"], df_curr.columns[1], label=df_curr.columns[1], s=3)
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("PV")
        ax.xaxis.set_major_locator(ticker.LinearLocator(5))
        ax.set_title("PVs vs. Time")
        ax.legend()
        plt.show()
        return None

    def plot_correlation(self, df: pd.DataFrame, pv_x: str, pv_y: str, start: str, end: str) -> None:
        """Plot the correlation of two PVs. 

        :param df: The DataFrame from which the PVs are plotted. 
        :param pv_x: The PV to be plotted on the x-axis. 
        :param pv_y: The PV to be plotted on the y-axis. 
        :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format
        :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format
        """

        # TODO: 
        # - width/height
        # - xlabel bottom, top
        # - ylabel left, right
        # - xlabel_color bottom, top
        # - ylabel_color left, right
        # - xlabel_font bottom, top
        # - ylabel_font left, right
        # - xlabel_fontsize bottom, top
        # - ylabel_fontsize left, right
        # - linecolors list
        # - linetypes list
        # - label list 
        # - datetime, algorithm to check what is changing, but changing the least (days, minutes, seconds, etc.)

        ax = plt.subplots(figsize=(10, 7), layout='constrained')
        # plot the correlation 
        ax = plt.subplots(figsize=(10, 7), layout='constrained')        
        ax.scatter(df[pv_x], df[pv_y], label=f"{pv_y} vs. {pv_x}", s=3)
        # tick settings
        x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[pv_x]]  # scientific notation
        y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in df[pv_y]]
        ax.set_xticklabels(x_ticks, fontsize=10)  # set tick labels
        ax.set_yticklabels(y_ticks, fontsize=10)
        ax.xaxis.set_major_locator(ticker.LinearLocator(5))
        ax.yaxis.set_major_locator(ticker.LinearLocator(5))
        # plot labels
        ax.set_xlabel(f"{pv_x}")
        ax.set_ylabel(f"{pv_y}")
        ax.set_title(f"{pv_y} vs. {pv_x}")
        ax.legend()
        plt.show()
        return None