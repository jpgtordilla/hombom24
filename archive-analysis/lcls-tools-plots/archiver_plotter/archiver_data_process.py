from pydantic import BaseModel, PositiveInt, ValidationInfo, field_validator
from typing import Annotated
from annotated_types import Len
import pandas as pd
from datetime import datetime
import sys

sys.path.append("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools")
import common.data_analysis.archiver as arch

MAX_YEAR_RANGE = 2


class PVModel(BaseModel):
    """Model class that contains parameters that define the pv_str and the start and end dates of the dataset.

    :param pv_str: The PV to plot.
    :param start: The start date of the plot in YYYY/MM/DD HH:MM:SS format.
    :param end: The end date of the plot in YYYY/MM/DD HH:MM:SS format.
    """

    pv_str: str
    start: str
    end: str

    @field_validator("pv_str")
    def check_pv_str(cls, pv_str: str) -> str:
        assert pv_str != "", "PV string is empty."
        assert ":" in pv_str, "PV string is invalid."
        return pv_str

    @field_validator("end", mode="after")
    def check_start_end_str(cls, end: str, info: ValidationInfo):
        start = info.data.get("start")
        assert start is not None, "Start date must be provided."
        assert end is not None, "Start date must be provided."
        assert start != "" and start != " ", "Start string is empty"
        assert end != "" and end != " ", "End string is empty."
        start_datetime = datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
        end_datetime = datetime.strptime(end, "%Y/%m/%d %H:%M:%S")
        current_datetime = datetime.now()
        assert start_datetime < current_datetime and end_datetime < current_datetime, "Invalid date, too far in future."
        assert start_datetime < end_datetime, "End date must be greater than start date."
        assert end_datetime.year - start_datetime.year <= 2, "Too long of a time range given."
        return end

    @property
    def pv_str(self):
        return self._pv_str

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @pv_str.setter
    def pv_str(self, value):
        self._pv_str = value

    @start.setter
    def start(self, value):
        self._start = value

    @end.setter
    def end(self, value):
        self._end = value


def pv(pv_str: str, start: str, end: str) -> PVModel:
    """Returns a PVModel instance."""
    return PVModel(pv_str=pv_str, start=start, end=end)


def get_formatted_timestamps(df_list: list[pd.DataFrame]) -> list[str]:
    """Removes redundant timestamp labels if they are the same throughout all the data points."""

    assert len(df_list) > 0, "DataFrame list is empty."
    date_list = df_list[0]["Timestamp"].tolist()
    # compares the first and last timestamp
    first_date = date_list[0]
    last_date = date_list[-1]
    date_format_list = ["%Y/", "%m/", "%d", " ", "%H:", "%M:", "%S"]
    # go character by character, comparing digits until they differ, then formatting appropriately
    for i in range(len(first_date)):
        curr_first_date = first_date[i]
        curr_last_date = last_date[i]
        # if the current year, month, day, etc. is not the same, then print the remaining timestamps on the axis
        if curr_first_date != curr_last_date:
            break
        if curr_first_date == "/" or curr_first_date == ":" or curr_last_date == " ":
            del date_format_list[0]
    date_format_str = "".join(date_format_list)
    # returns a list of reformatted timestamp strings that will be plotted
    return [datetime.strptime(date, "%Y/%m/%d %H:%M:%S").strftime(date_format_str) for date in date_list]


def create_df(pv_model: PVModel) -> pd.DataFrame:
    """Create and return a DataFrame given a PV and start/end date.

    Column titles of the DataFrame are "Timestamp" and the pv_str.
    """

    start = pv_model.start
    end = pv_model.end
    pv_str = pv_model.pv_str

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
    pv_clean_timestamps = [pv_timestamps[i].strftime(format_string) for i in
                           range(len(pv_timestamps))]  # clean and reformat timestamps from the dict
    return pd.DataFrame({"Timestamp": pv_clean_timestamps, pv_str: pv_values})  # create df with columns


def create_correlation_df(df_x: pd.DataFrame, df_y: pd.DataFrame) -> pd.DataFrame:
    """Given two DataFrames of PVs, return a single DataFrame with matching and aligned timestamps.

    :param df_y: The name of the PV or the DataFrame that will be plotted on the y-axis.
    :param df_x: The name of the PV that will be plotted on the x-axis.
    """
    if df_x.empty or df_y.empty:
        return pd.DataFrame()
    return pd.merge(df_y, df_x, on="Timestamp")  # merge DataFrames on equal timestamp strings
