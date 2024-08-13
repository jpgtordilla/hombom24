import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import random
# TODO: change to path to tools
import sys
# TODO: change path, refactor
sys.path.append(
    '/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools')
import common.data_analysis.archiver as arch  # type: ignore


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
            df_curr_charge = df[(df[pv_charge] - abs(charge) >= 0) & (((df[pv_charge] - abs(charge))/abs(charge)) <=
                                                                      tolerance)]
            df_list.append(df_curr_charge)
        return df_list
