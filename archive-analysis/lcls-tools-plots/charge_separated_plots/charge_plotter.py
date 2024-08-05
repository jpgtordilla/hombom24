import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from matplotlib import ticker
from matplotlib import cm
import pandas as pd
import numpy as np
import sys
from scipy.stats import gaussian_kde
from datetime import datetime
sys.path.append('/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/archiver_plotter')
import archiver_plotter as ap  # type: ignore


def create_clusters(df: pd.DataFrame, low_vary_column: str, error_tolerance: float) -> list[pd.DataFrame]:
    """Create a list of DataFrames, each with data points with similar x values but varying y values.

    :param df: DataFrame with at least and x_column and a y_column from which to create clusters.
    :param low_vary_column: String of the title of the column with points by which to create clusters.
    :param error_tolerance: The tolerance range of the x values in whatever units the x_column is.
    """

    df = df.sort_values(by=low_vary_column).reset_index(drop=True)

    # group the values by similar x values
    df_groups: list[pd.DataFrame] = []
    curr_group: list[pd.Series] = []

    for i, curr_row in df.iterrows():
        if not curr_group:
            curr_group.append(curr_row)  # add current row to the group if no rows added yet
        else:
            # if the row is not empty, check if the item in the cell in the x_column of the current row in within range
            if abs(curr_group[-1][low_vary_column] - curr_row[low_vary_column]) <= error_tolerance:
                curr_group.append(curr_row)
            else:
                # if it is out of range, add the current group as a DataFrame to the list
                df_groups.append(pd.DataFrame(curr_group))
                curr_group = [curr_row]  # create a new group with the new row

    # handle remaining rows and add to a DataFrame and then to the DataFrame list
    if curr_group:
        df_groups.append(pd.DataFrame(curr_group))

    return df_groups


def get_means_and_stds(df_groups: list[pd.DataFrame], high_vary_column: str) -> list[tuple[float, float]]:
    """Create a 2D list with means and standard deviations for each cluster.

    Returns a list of pairs (mean of each cluster, std for each cluster).

    :param df_groups: List of DataFrames, each one representing a different cluster.
    :param high_vary_column: String of the title of the column with the varying points in a cluster.
    """

    result = []
    for group_index in range(len(df_groups)):
        mean = float(np.mean(df_groups[group_index][high_vary_column]))
        curr_std = float(np.std(df_groups[group_index][high_vary_column]))
        result.append((mean, curr_std))
    return result


def get_data_in_range(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    start_obj = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end_obj = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    return df[(df["Timestamp"] >= start_obj) & (df["Timestamp"] <= end_obj)]


class ChargePlotter:
    def __init(self):
        return

    def remove_charges_below_value(self, df: pd.DataFrame, pv_charge: str, min_charge_value: float) -> pd.DataFrame:
        return df[df[pv_charge] >= min_charge_value]

    def merge_with_margin_on_timestamp(self, df_1: pd.DataFrame, df_2: pd.DataFrame, time_margin_seconds: float):
        """Merges two DataFrames on similar timestamps, where timestamps differ by less than the time specified by the
        time_margin parameter.

        Creates additional columns that store the time difference between the true and comparison timestamps.

        :param df_1: First DataFrame with a Timestamp column.
        :param df_2: Second DataFrame with a Timestamp column.
        :param time_margin_seconds: The time margin between two timestamps as given in seconds, useful for defining the
        propagated error for a correlation.
        """

        # must convert the values in the Timestamp column to datetime objects
        df_1["Timestamp"] = pd.to_datetime(df_1["Timestamp"])
        df_2["Timestamp"] = pd.to_datetime(df_2["Timestamp"])

        """Use the pandas method merge_asof to merge the DataFrames within a tolerance value 
        (pandas.pydata.org/docs/reference/api/pandas.merge_asof.html). 
        
        According to the pd.merge_asof() function, the first DataFrame parameter in the function defines what the second 
        DataFrame is compared to. 
        
        Therefore, the first DataFrame will have a time-axis uncertainty of 0. 
        The second DataFrame will have some uncertainty ranging from 0 to the time_margin_seconds value. 
        """

        # compute time difference between the second and first DataFrames and add a new column to the second DataFrame
        df_merged = pd.merge_asof(df_1, df_2, on="Timestamp", direction="nearest",
                                  tolerance=pd.Timedelta(f"{time_margin_seconds}s"))
        df_merged[f"{df_2.columns[1]} Time Uncert"] = df_merged[df_2.columns[1]] - df_merged[
            df_1.columns[1]]  # get time uncertainty

        # Convert values in the Timestamp column back to String objects, remove NaN rows, and return
        timestamp_list = df_merged["Timestamp"].to_list()
        df_merged["Timestamp"] = timestamp_list
        return df_merged.dropna(how="any")

    def plot_correlation(self,
                         df: pd.DataFrame,
                         pv_y: str,
                         pv_x: str,
                         pv_charge: str,
                         charge_val: float,
                         charge_tolerance: float,
                         plot_error_bars: bool,
                         low_vary_column: str,
                         error_tolerance: float,
                         x_label: str,
                         y_label: str,
                         label_size: int = 24,
                         y_vary=True,
                         x_num_rounded_digits: int = 5,
                         y_num_rounded_digits: int = 5,
                         x_units: str = "",
                         y_units: str = "",
                         x_change_decimal_point: int = 0,
                         y_change_decimal_point: int = 0,
                         same_day=False,
                         overlay=False):
        """Plots the correlation between two columns in a DataFrame, separated by a specific charge value (pC).

        DataFrame will be modified to only include rows that contain a charge value within a given tolerance percentage
        range (0.0-1.0).

        Charge-separation:

        :param df: DataFrame with a Timestamp column and an arbitrary amount of PV columns.
        :param pv_y: String representation of the PV to be plotted on the y-axis.
        :param pv_x: String representation of the PV to be plotted on the x-axis.
        :param pv_charge: String representation of the charge PV by which to filter the DataFrame.
        :param charge_val: The charge value in pC by which to separate out rows.
        :param charge_tolerance: The percentage tolerance between 0.0-1.0 (inclusive) to inform how large of a spread of
        charge values are kept in the DataFrame.

        Error bars:

        :param plot_error_bars: Boolean flag specifying whether to plot the error bars.
        :param low_vary_column: String of the title of the column with points by which to create clusters.
        :param error_tolerance: The tolerance range of the x values in whatever units the x_column is.
        :param y_vary: Boolean indicating if the y_column is varying or not.

        Axis label customization:

        :param x_label: String representation of the x-axis label.
        :param y_label: String representation of the y-axis label.

        :param label_size: Integer representing the size of the labels in points.
        :param x_num_rounded_digits: Optional, Number of digits to round off the x-axis values.
        :param y_num_rounded_digits: Optional, Number of digits to round off the y-axis values.
        :param x_units: Optional, String representation of the x-axis units.
        :param y_units: Optional, String representation of the y-axis units.
        :param x_change_decimal_point: Optional, positive integer raises the x-axis labels by orders of magnitude,
        negative decreases.
        :param y_change_decimal_point: Optional, positive integer raises the y-axis labels by orders of magnitude,
        negative decreases.
        :param same_day: Optional, Boolean flag specifying whether the data takes place on the same day.

        Overlay:
        :param overlay: Boolean flag specifying whether to overlay the mean data plots.
        """

        # filter out unwanted charges
        df_charge_filtered = df[(df[pv_charge] >= charge_val - (charge_val * charge_tolerance)) & (
                df[pv_charge] <= charge_val + (charge_val * charge_tolerance))]
        fig, ax = plt.subplots(figsize=(12, 10))
        # plot correlation points
        x = df_charge_filtered[pv_x]
        y = df_charge_filtered[pv_y]

        if overlay:
            # plot cluster points
            df_groups: list[pd.DataFrame] = create_clusters(df, low_vary_column, error_tolerance)
            means_and_stds: list[(float, float)] = get_means_and_stds(df_groups, "SCOP:AMRF:RF01:AI_MEAS1")

            y_cluster_points = []
            x_cluster_points = []
            if y_vary:  # if the points in the y_column are the varying points in a cluster
                y_cluster_points = [cluster[0] for cluster in means_and_stds]  # average y val in each cluster
                x_cluster_points = [float(np.mean(df_groups[df][pv_x])) for df in
                                    range(len(df_groups))]  # average x val in each cluster
            else:
                y_cluster_points = [float(np.mean(df_groups[df][pv_y])) for df in
                                    range(len(df_groups))]  # average y val in each cluster
                x_cluster_points = [cluster[0] for cluster in means_and_stds]  # average x val in each cluster

            # xy = np.vstack([x, y])
            # z = gaussian_kde(xy)(xy)
            # ax.scatter(x, y, c=z, cmap="viridis")
            ax.scatter(x, y, color="blue")

            # create a line of best fit
            slope, intercept = np.polyfit(x, y, deg=1)
            ax.axline(xy1=(0, intercept), slope=slope, label=f"y = {slope:.3f}x + {intercept:.3f}", color="blue")

            # x_cluster_y_cluster = np.vstack([x_cluster_points, y_cluster_points])
            # z = gaussian_kde(x_cluster_y_cluster)(x_cluster_y_cluster)
            # ax.scatter(x_cluster_points, y_cluster_points, c=z, cmap="plasma")
            ax.scatter(x_cluster_points, y_cluster_points, color="red")
            # create a line of best fit
            slope, intercept = np.polyfit(x_cluster_points, y_cluster_points, deg=1)
            ax.axline(xy1=(0, intercept), slope=slope, label=f"y = {slope:.3f}x + {intercept:.3f}", color="red")

            # plot error bars
            error = [cluster[1] for cluster in means_and_stds]
            ax.errorbar(x_cluster_points, y_cluster_points, yerr=error, ls="none", ecolor="red")

        if plot_error_bars and not overlay:
            # plot cluster points
            df_groups: list[pd.DataFrame] = create_clusters(df, low_vary_column, error_tolerance)
            means_and_stds: list[(float, float)] = get_means_and_stds(df_groups, "SCOP:AMRF:RF01:AI_MEAS1")

            y_cluster_points = []
            x_cluster_points = []
            if y_vary:  # if the points in the y_column are the varying points in a cluster
                y_cluster_points = [cluster[0] for cluster in means_and_stds]  # average y val in each cluster
                x_cluster_points = [float(np.mean(df_groups[df][pv_x])) for df in
                                    range(len(df_groups))]  # average x val in each cluster
            else:
                y_cluster_points = [float(np.mean(df_groups[df][pv_y])) for df in
                                    range(len(df_groups))]  # average y val in each cluster
                x_cluster_points = [cluster[0] for cluster in means_and_stds]  # average x val in each cluster

            # xy = np.vstack([x, y])
            # z = gaussian_kde(xy)(xy)
            # ax.scatter(x, y, c=z, cmap="viridis")
            ax.scatter(x_cluster_points, y_cluster_points)
            # create a line of best fit
            slope, intercept = np.polyfit(x_cluster_points, y_cluster_points, deg=1)
            ax.axline(xy1=(0, intercept), slope=slope, label=f"y = {slope:.3f}x + {intercept:.3f}", color="red")

            # plot error bars
            error = [cluster[1] for cluster in means_and_stds]
            ax.errorbar(x_cluster_points, y_cluster_points, yerr=error, ls="none", color="red")
        elif not overlay and not plot_error_bars:
            xy = np.vstack([x, y])
            z = gaussian_kde(xy)(xy)
            ax.scatter(x, y, c=z, cmap="viridis")
            fig.colorbar(cm.ScalarMappable(cmap="viridis"), ax=ax)  # add colorbar
            # ax.scatter(x, y)
            # create a line of best fit
            slope, intercept = np.polyfit(x, y, deg=1)
            ax.axline(xy1=(0, intercept), slope=slope, label=f"y = {slope:.3f}x + {intercept:.3f}", color="red")

        # set labels
        start_date = str(df_charge_filtered["Timestamp"].to_list()[0])[:10]
        end_date = str(df_charge_filtered["Timestamp"].to_list()[-1])[:10]
        start_time = str(df_charge_filtered["Timestamp"].to_list()[0])[12:]
        end_time = str(df_charge_filtered["Timestamp"].to_list()[-1])[12:]

        ax.set_title(f"{y_label} vs. {x_label}\nfor {charge_val}pC from {start_date} to {end_date}",
                     fontsize=label_size + (label_size*0.1))
        # if not same_day:
        #     ax.set_title(f"{y_label} vs. {x_label}\nfor {charge_val}pC from {start_date} to {end_date}",
        #                  fontsize=label_size)
        # else:
        #     ax.set_title(f"{y_label} vs. {x_label}\nfor {charge_val}pC from {start_time} to {end_time}",
        #                  fontsize=label_size)

        ax.set_xlabel(f"{x_label} {x_units}", fontsize=label_size)
        ax.set_ylabel(f"{y_label} {y_units}", fontsize=label_size)

        # set ticks
        x_digit_round_string = f"{{x:,.{x_num_rounded_digits}f}}"
        y_digit_round_string = f"{{x:,.{y_num_rounded_digits}f}}"
        ax.xaxis.set_major_formatter(StrMethodFormatter(x_digit_round_string))
        ax.yaxis.set_major_formatter(StrMethodFormatter(y_digit_round_string))
        # change values of x-axis or y-axis ticks to a different order of magnitude
        x_tick_locs = list(ax.get_xticks())
        y_tick_locs = list(ax.get_yticks())
        x_tick_labels = [float(tick.get_text().replace('−', '-')) for tick in ax.get_xticklabels()]
        y_tick_labels = [float(tick.get_text().replace('−', '-')) for tick in ax.get_yticklabels()]
        # raise or lower to the given power
        x_tick_labels_new = [round(x * (10 ** x_change_decimal_point), x_num_rounded_digits) for x in x_tick_labels]
        # raise or lower to the given power
        y_tick_labels_new = [round(y * (10 ** y_change_decimal_point), y_num_rounded_digits) for y in y_tick_labels]
        ax.xaxis.set_major_locator(ticker.FixedLocator(x_tick_locs))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(x_tick_labels_new))
        ax.yaxis.set_major_locator(ticker.FixedLocator(y_tick_locs))
        ax.yaxis.set_major_formatter(ticker.FixedFormatter(y_tick_labels_new))
        ax.tick_params(axis="x", labelsize=20)
        ax.tick_params(axis="y", labelsize=20)
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # reduce the amount of ticks for both axes
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax.legend(fontsize=label_size - (label_size*0.2))
        plt.subplots_adjust(left=0.15, bottom=0.15)
        plt.show()
