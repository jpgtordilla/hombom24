import sys
# TODO: change to relative path within lcls_tools
sys.path.append(
    '/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools')
import common.data_analysis.archiver as arch  # type: ignore
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class ArchiverPlotter:
    def __init__(self):
        self.font_x = {
            "family": "",
            "color": "",
            "size": 16
        }
        self.font_y = {
            "family": "",
            "color": "",
            "size": 16
        }
        self.font_title = {
            "family": "",
            "color": "",
            "size": 20
        }
        self.label_settings = {
            "y_axis": "",
            "x_axis": ""
        }
        return

    def set_fonts(self, label_font, xlabel_color, ylabel_color, title_color):
        """Sets font instance variables."""
        self.font_x["family"] = label_font
        self.font_y["family"] = label_font
        self.font_title["family"] = label_font
        self.font_x["color"] = xlabel_color
        self.font_y["color"] = ylabel_color
        self.font_title["color"] = title_color

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

    """PLOTTING METHODS"""

    def plot_pv_over_time(self,
                          df_list: list[pd.DataFrame],
                          width=10,
                          height=7,
                          xlabel_bottom="Timestamp",
                          ylabel_left="PV",
                          xlabel_color="black",
                          ylabel_color="black",
                          title_color="black",
                          label_font="Helvetica",
                          pv_colors=("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"),
                          line_types=("solid", "dashed", "dashdot", "dotted"),
                          marker_types=("x", ".", "^", "s", "p", "*"),
                          is_scatter=False,
                          is_marker=False,
                          marker_size=5,
                          pv_labels=None,
                          num_ticks=7,
                          smart_title=False) -> None:
        """Plots a nonempty list of PVs over time.

        :param df_list: A list of DataFrames from which to plot the PVs.

        :param width: The width of the plot to be rendered. 
        :param height: The height of the plot to be rendered. 
        :param xlabel_bottom: The label that will be on the bottom of the plot.
        :param ylabel_left: The label that will be to the left of the plot.
        :param xlabel_color: The color of the x label/s.
        :param ylabel_color: The color of the y label/s.
        :param title_color: The color of the title.
        :param label_font: The font for all the labels for the plot. 
        :param pv_colors: A list of colors for each pv that is plotted, in the order of df_list. 
        :param line_types: A list of all line types for each pv that is plotted, in the order of df_list.
        :param marker_types: A list of all markers for each pv that is plotted, in the order of df_list.
        :param is_scatter: A boolean for whether to plot all points as scatter, or to plot as lines.
        :param is_marker: A boolean for whether to plot all points as markers.
        :param marker_size: The size of the scatter marker, if scatter is chosen as a line_types option. 
        :param pv_labels: A list of labels for each PV, in the order of df_list.
        :param num_ticks: The number of ticks along the x-axis of the plot.
        :param smart_title: A boolean for whether to list the PVs in the title.
        """

        fig, ax = plt.subplots(figsize=(width, height), layout="constrained")

        # LEGEND LABELS
        if pv_labels is not None:
            for i in range(len(df_list)):
                df_curr = df_list[i]
                df_curr.rename(columns={df_curr.columns[1]: pv_labels[i]}, inplace=True)

        # LABELS
        ax.xaxis.set_major_locator(ticker.LinearLocator(num_ticks))
        ax.yaxis.set_major_locator(ticker.LinearLocator(num_ticks))
        self.set_fonts(label_font, xlabel_color, ylabel_color, title_color)
        plt.xlabel(xlabel_bottom, fontdict=self.font_x)
        plt.ylabel(ylabel_left, fontdict=self.font_y)

        # TITLE
        if not smart_title:
            plt.title("PVs vs. Time", fontdict=self.font_title)
        else:
            # create a title using the PV names
            pv_list = [df_curr.columns[1] for df_curr in df_list]
            plt.title(f"{", ".join(pv_list)} vs. Time", fontdict=self.font_title)

        # PLOTTING
        for i in range(len(df_list)):  # plot each DataFrame in df_list
            df_curr = df_list[i]  # current DataFrame plotted
            col = df_curr.columns[1]  # y-axis Series for each of the DataFrames
            if not is_scatter:  # line plot
                # choose a line type and plot accordingly
                curr_line_type = line_types[i % len(line_types)]  # cycle through the list
                # marker plot
                if is_marker:
                    ax.plot(df_curr["timestamps"], df_curr[col], color=pv_colors[i % len(pv_colors)],
                            linestyle=curr_line_type, label=col,
                            marker=marker_types[i % len(marker_types)], markersize=marker_size)
                # line plot
                else:
                    ax.plot(df_curr["timestamps"], df_curr[col], color=pv_colors[i % len(pv_colors)],
                            linestyle=curr_line_type, label=col)
            # scatter plot
            else:
                ax.scatter(df_curr["timestamps"], df_curr[col], label=col, s=marker_size)

        ax.legend()
        plt.show()
        return None

    def plot_correlation(self,
                         df: pd.DataFrame,
                         pv_x: str,
                         pv_y: str,
                         width=10,
                         height=7,
                         xlabel_color="black",
                         ylabel_color="black",
                         title_color="black",
                         label_font="Helvetica",
                         correl_color="tab:blue",
                         line_type="solid",
                         marker_type=".",
                         is_scatter=True,
                         is_marker=False,
                         marker_size=5,
                         pv_xlabel=None,
                         pv_ylabel=None,
                         num_ticks=7,
                         smart_labels=False) -> None:
        """Plot the correlation of two PVs. 

        :param df: The DataFrame from which the PVs are plotted. 
        :param pv_x: The PV to be plotted on the x-axis. 
        :param pv_y: The PV to be plotted on the y-axis.

        :param width: The width of the plot to be rendered.
        :param height: The height of the plot to be rendered.
        :param xlabel_color: The color of the x label/s.
        :param ylabel_color: The color of the y label/s.
        :param title_color: The color of the title.
        :param label_font: The font for all the labels for the plot.
        :param correl_color: The color of the correlation plot.
        :param line_type: The default line type for the plot.
        :param marker_type: The default marker type for the plot.
        :param is_scatter: A boolean for whether to plot all points as scatter, or to plot as lines.
        :param is_marker: A boolean for whether to plot all points as markers.
        :param marker_size: The size of the scatter marker, if scatter is chosen as a line_types option.
        :param pv_xlabel: The label for the x-axis.
        :param pv_ylabel: The label for the y-axis.
        :param num_ticks: The number of ticks along the x-axis of the plot.
        :param smart_labels: A boolean for whether to list the PVs in the title.
        """

        fig, ax = plt.subplots(figsize=(width, height), layout="constrained")

        # LEGEND LABELS
        if pv_xlabel and pv_ylabel is not None:
            df.rename(columns={pv_x: pv_xlabel, pv_y: pv_ylabel}, inplace=True)

        # LABELS
        if smart_labels and pv_xlabel and pv_ylabel is not None:
            self.label_settings["y_axis"] = pv_ylabel
            self.label_settings["x_axis"] = pv_xlabel

        self.set_fonts(label_font, xlabel_color, ylabel_color, title_color)
        plt.title(f"{self.label_settings["y_axis"]} vs. {self.label_settings["x_axis"]}", fontdict=self.font_title)
        plt.xlabel(self.label_settings["x_axis"], fontdict=self.font_x)
        plt.ylabel(self.label_settings["y_axis"], fontdict=self.font_y)

        ax.xaxis.set_major_locator(ticker.LinearLocator(num_ticks))
        ax.yaxis.set_major_locator(ticker.LinearLocator(num_ticks))

        # PLOTTING
        if not is_scatter:  # line plot
            # with marker
            if is_marker:
                ax.plot(df[pv_xlabel], df[pv_ylabel], color=correl_color, linestyle=line_type, marker=marker_type,
                        markersize=marker_size)
            # without marker
            else:
                ax.plot(df[pv_xlabel], df[pv_ylabel], color=correl_color, linestyle=line_type)
        # scatter plot
        else:
            ax.scatter(df[pv_xlabel], df[pv_ylabel], color=correl_color, s=marker_size)

        plt.show()
        return None
