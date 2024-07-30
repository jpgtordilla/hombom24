import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import random
# TODO: change to path to tools
import sys

sys.path.append(
    '/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools')
import common.data_analysis.archiver as arch  # type: ignore

"""
TODO: determine whether MEME yields better results
Until then, we will keep the following code commented and unchanged. 
A temporary replacement that analyzes data from the EPICS Archiver will be used until further notice. 
"""

'''
# TODO: at 2E3, generates the same resolution as EPICS Archiver, but 20 times slower
DATA_LIMIT = 2E3  # the max amount of data that can be requested in a single occurrence
INTERVAL_SAMPLE_SIZE = 100  # number of points from which the average interval between data points is calculated


def get_days_between_datetime(start: str, end: str) -> int:
    # determine the amount of days between the start and end datetime
    format_string = "%Y/%m/%d %H:%M:%S"
    start_obj = datetime.strptime(start, format_string)
    end_obj = datetime.strptime(end, format_string)
    num_days = (end_obj - start_obj).days
    return num_days


def predict_points_for_timeframe(pv_str: str, start_time: str, end_time: str) -> int:
    """Helper method that predicts and returns the amount of points generated within a given timeframe when a PV
    is requested.

    This function is used by another helper function, predict_points_for_timeframe_per_period, because the amount of
    datapoints generated for a PV per month or week varies greatly. This can be tuned in the future depending on if
    more long-term data will be stored with the archiver.
    """

    format_string = "%Y/%m/%d %H:%M:%S"
    start_obj = datetime.strptime(start_time, format_string)
    end_obj = datetime.strptime(end_time, format_string)

    # ERROR HANDLING
    if (end_obj - start_obj).days <= 0:
        raise ValueError("End time must be greater than (occur after) start time.")

    x = []  # store the days
    y = []  # store the number of data points generated for an amount of days elapsed
    for i in range(1, 4):
        # set date interval to be increasing longer by a day
        interval_obj = start_obj + timedelta(days=i)
        # time the request
        start_timer = time.time()
        arch_data = arch.get_values_over_time_range([pv_str], start_obj, interval_obj)
        end_timer = time.time()
        # add the data point so it can be graphed
        time_request = round((end_timer - start_timer), 4)
        num_days = i - 1
        num_data_points = len(arch_data[pv_str].values)  # number of requested values
        # cache points for the estimate
        x.append(num_days)
        y.append(num_data_points)
    # want to know how many data points generated in the given timeframe
    m, b = np.polyfit(x, y, deg=1)
    num_days = (end_obj - start_obj).days
    num_points_projected = float(m * num_days + b)
    return int(round(num_points_projected))


def predict_points_for_timeframe_per_period(pv_str: str, start_time: str, end_time: str, period_in_days: int) -> int:
    """Helper function that uses the predict_points_for_timeframe helper function to determine the amount of points
    generated within a given timeframe when a PV is requested, over a multi-period_in_days amount of time.
    """

    # determine the amount of days between the start and end datetime
    num_days = get_days_between_datetime(start_time, end_time)

    # every period_in_days days, predict how many points are generated for that period
    num_points = 0
    day_index = 0
    while day_index < num_days:
        # get the datetime object for the current day
        format_string = "%Y/%m/%d %H:%M:%S"
        current_time_obj = datetime.strptime(start_time, format_string) + timedelta(days=day_index)
        current_time_string = current_time_obj.strftime(format_string)
        # if there are less than 30 days left, predict the amount of points generated for the remaining time
        if day_index + period_in_days >= num_days:
            num_points += predict_points_for_timeframe(pv_str, current_time_string, (current_time_obj +
                                                       timedelta(days=(num_days - day_index))).strftime(format_string))
            break
        if day_index % period_in_days == 0 or day_index == 1:
            num_points += predict_points_for_timeframe(pv_str, current_time_string, (current_time_obj +
                                                       timedelta(days=period_in_days)).strftime(format_string))
            day_index += period_in_days
    return num_points


def request_data_interval(pv_str: str, day: str, sample_size: int) -> float:
    """Get the amount of seconds between data points for a given PV on a given day.

    Makes a request for a PV and gets the average interval (in seconds) between data points for a given sample size.
    """

    # set the range of data and make a request
    start_str = f"{day} 00:00:00"
    end_str = f"{day} 23:59:59"
    start_time = datetime.strptime(start_str, "%Y/%m/%d %H:%M:%S")
    end_time = datetime.strptime(end_str, "%Y/%m/%d %H:%M:%S")
    arch_data = arch.get_values_over_time_range([pv_str], start_time, end_time)

    # get the list of timestamps and get the average interval based on the sample size
    intervals = []
    timestamps = arch_data[pv_str].timestamps

    # handling the case in which an empty or very small timestamps list is returned
    if len(timestamps) <= 2:
        return 0

    for i in range(sample_size):
        random_first_index = random.randint(0, len(timestamps) - 2)
        second_index = random_first_index + 1
        interval = (timestamps[second_index] - timestamps[random_first_index]).total_seconds()
        intervals.append(interval)

    return float(np.mean(intervals))


def get_data_interval_dict(pv_str: str, start_time: str, end_time: str, period_in_days: int) \
        -> dict[float: list[datetime]]:
    """Gets the time interval between data points in a dataset. Finds the time interval between the first two data
    points for each period_in_days and returns a list of intervals (in seconds).

    Dictionary takes the form of: {interval: [start, end]}
    """

    # determine the amount of days between the start and end datetime
    num_days = get_days_between_datetime(start_time, end_time)

    interval_dict = {}
    # every period_in_days days, get the time interval between the first two data points
    day_index = 0
    while day_index < num_days:
        # get the datetime object for the current day
        format_string = "%Y/%m/%d %H:%M:%S"
        current_time_obj = datetime.strptime(start_time, format_string) + timedelta(days=day_index)
        current_time_string = current_time_obj.strftime(format_string)
        # if there are less than 30 days left, get the interval between the next two data points
        if day_index + period_in_days >= num_days:
            # get interval
            interval = request_data_interval(pv_str, current_time_obj.strftime("%Y/%m/%d"), INTERVAL_SAMPLE_SIZE)
            # add to interval dict
            interval_dict[interval] = [current_time_obj, current_time_obj + timedelta(days=(num_days - day_index))]
            break
        # for each period, get the interval between the first two data points in that period
        if day_index % period_in_days == 0 or day_index == 1:
            # get interval
            interval = request_data_interval(pv_str, current_time_obj.strftime("%Y/%m/%d"), INTERVAL_SAMPLE_SIZE)
            # add to interval dict
            interval_dict[interval] = [current_time_obj, current_time_obj + timedelta(days=period_in_days)]
            day_index += period_in_days

    return interval_dict
'''

# EPICS ARCHIVER PEAK ANALYSIS


def return_peak_areas_list(df: pd.DataFrame) -> list[list[datetime]]:
    """Returns a 2D list of pairs of datetime objects that will be used to request data for only the peak areas."""
    pass


def create_clusters_from_list(vals, tolerance) -> list:
    """Returns a 2D list, where each sub-list represents a cluster full of similar charges."""
    vals.sort()
    clusters = [[]]
    cluster_index = 0
    comparison = vals.pop(0)  # initial comparison is the first value in the given charge list
    clusters[cluster_index].append(comparison)
    while len(vals) > 0:
        for i in range(len(vals)):
            next_val = vals.pop(0)
            # if next_val is within percentage of comparison's value
            if abs(next_val - comparison) <= (tolerance * comparison):
                clusters[cluster_index].append(next_val)  # add next_val to cluster
            else:
                cluster_index += 1  # index the next cluster
                clusters.append([])  # add a new empty list
                clusters[cluster_index].append(next_val)  # add next_val to the next cluster
                comparison = next_val  # this first value of the next cluster becomes the next comparison
                break

    return clusters


class ChargeSeparator:
    def __init__(self):
        self.current_charges = []  # updated whenever a DataFrame is separated by charges
        return

    @property
    def current_charges(self):
        return self._current_charges

    @current_charges.setter
    def current_charges(self, charge_list: list[float]):
        self._current_charges = charge_list

    '''
    def create_df(self, pv: str, start: str, end: str, period_in_days: int) -> pd.DataFrame:
        """Helper method that returns a simplified DataFrame over a typically long period of time.

        Makes a few requests, projects the amount for the desired timeframe, and divides this by a constant around
        the IOPub data rate to get the ratio of the total amount of projected data points to the desired amount of
        data points. Then a request is made by taking the interval between data points from the initial request and
        multiplying it by this ratio, giving us the time between data points.

        Makes use of multiple helper functions in this order:
        1. predict_points_monthly_for_timeframe
            a. predict_points_for_timeframe
        2. get_data_interval_dict
            b. request_data_interval

        :param pv: The string representation of the requested PV.
        :param start: The string representation of the start datetime in YYYY/MM/DD HH:MM:SS format.
        :param end: The string representation of the end datetime in YYYY/MM/DD HH:MM:SS format.
        :param period_in_days: The number of days between great differences in how many data points are generated for a PV.
        """
        format_string = "%Y/%m/%d %H:%M:%S"
        projected_num_points = predict_points_for_timeframe_per_period(pv, start, end, period_in_days)
        total_to_desired_ratio = 1
        if projected_num_points > DATA_LIMIT:
            total_to_desired_ratio = round(projected_num_points / DATA_LIMIT)

        df_list = []
        # get the intervals between each group of data and create separate DataFrames for each group
        interval_dict = get_data_interval_dict(pv, start, end, period_in_days)
        timestamps = list(interval_dict.values())
        datetime_range_index = 0
        for interval in interval_dict.keys():
            if interval == 0:  # handling case where an empty timestamps list is returned
                continue
            delta = round(interval * total_to_desired_ratio)  # the time_delta argument to use in the archiver request
            current_range = timestamps[datetime_range_index]
            start_obj = current_range[0]
            end_obj = current_range[-1]
            # make a data request for the entire timeframe, with a set delta
            # TODO: diagnose the issue here and potentially replace it with something else, in theory this should work!
            data_interval = arch.get_data_with_time_interval([pv], start_obj, end_obj,
                                                             time_delta=timedelta(seconds=delta))
            # create a DataFrame from this request
            pv_dict = data_interval[pv]
            pv_timestamps = pv_dict.timestamps
            pv_values = pv_dict.values
            pv_clean_timestamps = [pv_timestamps[i].strftime(format_string) for i in
                                   range(len(pv_timestamps))]  # clean and reformat timestamps from the dict
            df_curr = pd.DataFrame({"timestamps": pv_clean_timestamps, pv: pv_values})  # create df with columns
            df_list.append(df_curr)
            datetime_range_index += 1  # go to the next pair of timestamps

        return pd.concat(df_list)
    '''

    def separate_df_by_charges(self, df: pd.DataFrame, pv_charge: str, tolerance: float = 0.1) -> list[pd.DataFrame]:
        """Given a DataFrame of PV data with a column for the PV values and charge values, this method separates
        the data by charge value and returns a list of DataFrames, each containing PV data over time for a given charge.

        Can be given a DataFrame with either one PV in addition to the charge PV, or multiple non-charge PVs.

        :param df: Pandas DataFrame with columns for the PV/s of interest and one column for the charge values.
        :param pv_charge: The string representation of the charge PV.
        :param tolerance: The percentage tolerance that will be used to determine the range of charges in each cluster.
        """

        df_list = []  # the list of charge-separated DataFrames to return
        charge_list = df[pv_charge].tolist()
        charge_clusters = create_clusters_from_list(charge_list, tolerance)
        charge_vals = [cluster[0] for cluster in charge_clusters]  # first charge in each cluster, to use for comparison
        self.current_charges = charge_vals
        for charge in charge_vals:
            # keep rows with charges within the tolerance range and add to the df_list
            df_curr_charge = df[(df[pv_charge] - abs(charge) >= 0) & (((df[pv_charge] - abs(charge))/abs(charge)) <= tolerance)]
            df_list.append(df_curr_charge)
        return df_list
