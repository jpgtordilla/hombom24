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

    """HELPER METHODS FOR PLOTTING""" 

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

    @staticmethod 
    def get_smart_ticks(timestamps: pd.Series) -> dict{str: float}: 
        """Returns a list of dictionary with float values and a string describing what they represent."""
        # TODO: define smart ticks function 
        pass 

        
    """PLOTTING METHODS"""
    def plot_pv_over_time(self, 
                          df_list: list[pd.DataFrame], 
                          start: str, 
                          end: str, 
                          width=10: int, 
                          height=7: int, 
                          xlabel_bottom="Timestamp": str, 
                          xlabel_top=None: str, 
                          ylabel_left="PV": str, 
                          ylabel_right=None: str, 
                          xlabel_color_botom="black": str, 
                          xlabel_color_top=None: str, 
                          ylabel_color_left="black": str, 
                          ylabel_color_right=None: str, 
                          label_font="Helvetica": str,  
                          pv_colors=["red", "green", "blue", "black"]: list[str], 
                          line_types=["-", "-.", "--", "--x"]: list[str], 
                          is_scatter=False, 
                          marker_size=3, 
                          labels=None: list[str], 
                          smart_ticks=False: boolean) -> None:
        """Plots a nonempty list of PVs over time.

        :param df_list: A list of DataFrames from which to plot the PVs. 
        :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format.
        :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format.

        :param width: The width of the plot to be rendered. 
        :param height: The height of the plot to be rendered. 
        :param xlabel_bottom: The label that will be on the bottom of the plot. 
        :param xlabel_top: The label that will be on the top of the plot. 
        :param ylabel_left: The label that will be to the left of the plot. 
        :param ylabel_right: The label that will be to the right of the plot. 
        :param xlabel_color_bottom: The color of the x label on the bottom of the plot. 
        :param xlabel_color_top: The color of the x label on the top of the plot. 
        :param ylabel_color_left: The color of the y label to the left of the plot. 
        :param ylabel_color_right: The color of the y label to the right of the plot. 
        :param label_font: The font for all the labels for the plot. 
        :param pv_colors: A list of colors for each pv that is plotted, in the order of df_list. 
        :param line_types: A list of all line types for each pv that is plotted, in the order of df_list. 
        :param is_scatter: A boolean for whether or not to plot all points as scatter, or to plot as lines. 
        :param marker_size: The size of the scatter marker, if scatter is chosen as a line_types option. 
        :param labels: A list of labels for each PV, in the order of df_list. 
        :param smart_ticks: A boolean for whether or not to display ticks for the time unit that changes, but changes the least. 
        :param smart_title: A boolean for whether or not to list the PVs in the title. 
        """

        # TODO: program remaining default parameters: 
        # - xlabel_bottom
        # - xlabel_top
        # - ylabel_left
        # - ylabel_right
        # - xlabel_color_bottom
        # - xlabel_color_top
        # - ylabel_color_left
        # - ylabel_color_right
        # - label_font
        # - pv_colors
        # - labels
        # - smart_ticks

        # PLOTTING
        ax = plt.subplots(figsize=(width, height), layout="constrained") 
        for i in range(len(df_list)): # plot each DataFrame in df_list
            df_curr = df_list[i]
            if not is_scatter: 
                # choose a line type and plot accordingly
                curr_line_type = line_types[i % len(line_types)] # cycle through the line_types list 
                ax.plot(df_curr["timestamps"], df_curr.columns[1], linestyle=curr_line_type, label=df_curr.columns[1], markersize=marker_size)
            else: 
                ax.scatter(df_curr["timestamps"], df_curr.columns[1], label=df_curr.columns[1], s=marker_size)

        # TICKS
        if not smart_ticks: 
            ax.xaxis.set_major_locator(ticker.LinearLocator(5))
        else: 
            # TODO: use smart ticks function 
            pass 

        # LABELS
        ax.set_xlabel(xlabel_bottom)
        ax.set_ylabel(ylabel_left)
        # set the title 
        ax.legend()
        if not smart_title: 
            ax.set_title("PVs vs. Time")
        else: 
            # create a title using the PV names
            pv_list = [df_curr.columns[1] for df_curr in df_list]
            ax.set_title(f"{", ".join(pv_list)} vs. Time")

        plt.show()
        return None

    def plot_correlation(self, 
                         df: pd.DataFrame, 
                         pv_x: str, 
                         pv_y: str, 
                         start: str, 
                         end: str) -> None:
        """Plot the correlation of two PVs. 

        :param df: The DataFrame from which the PVs are plotted. 
        :param pv_x: The PV to be plotted on the x-axis. 
        :param pv_y: The PV to be plotted on the y-axis. 
        :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format
        :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format
        """

        # TODO: create and program all default parameters

        # plot the correlation 
        ax = plt.subplots(figsize=(10, 7), layout="constrained")        
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