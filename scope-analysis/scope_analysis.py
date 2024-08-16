from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
from scipy.signal import butter, filtfilt, decimate


def clean_df(path: str) -> pd.DataFrame:
    """Clean the fast-scope dataframe so that it has proper column titles."""
    path_df = pd.read_csv(path)
    # duplicate the first row
    path_df.loc[-1] = path_df.columns.tolist()
    path_df.index = path_df.index + 1
    path_df = path_df.sort_index()
    # rename columns
    df_result = path_df.rename(columns={f"{path_df.columns[0]}": "info", f"{path_df.columns[1]}": "info_vals",
                                        f"{path_df.columns[2]}": "info_units", f"{path_df.columns[3]}": "time",
                                        f"{path_df.columns[4]}": "values"})
    return df_result


def plot_df(signal_df, t_col, v_col):
    """Plot the dataframe with values over time to visualize the data."""
    figure, axes = plt.subplots(figsize=(20, 5))
    # cast columns to float
    t = signal_df[t_col].astype("float")
    v = signal_df[v_col].astype("float")
    # plot signal
    axes.plot(t, v, linestyle='-', linewidth=0.1)
    plt.show()


# cannot rewrite with parameters, must be re-structured depending on filenames and local locations
def create_full_df():
    """Create a large pandas DataFrame with "time" and "values" columns
    order: set2_cav1, set2_cav2, set3_cav1, set3_cav2, etc.
    column names: time_set2_cav1 and values_set2_cav1, etc.

    Algorithm:
    rename the time and values columns for set2_cav1 (time_set2_cav1 and values_set2_cav1)
    remove the other columns from set2_cav1
    for the rest of the files:
    - rename their time and values columns following the naming convention
    - remove their non-time and non-values columns
    - add those columns to the aggregate DataFrame
    return the resulting DataFrame
    """

    df_set2_cav1 = clean_df(
        "/Users/jonathontordilla/Desktop/hombom24/scope-analysis/2024-07-03_fast_scope/set2_cav1.csv")
    rename_df_set2_cav1 = df_set2_cav1.rename(columns={"time": "time_set2_cav1", "values": "values_set2_cav1"})
    clean_df_set2_cav1 = rename_df_set2_cav1.loc[0:len(rename_df_set2_cav1["time_set2_cav1"]),
                                                 "time_set2_cav1": "values_set2_cav1"]

    df_set2_cav2 = clean_df(
        "/Users/jonathontordilla/Desktop/hombom24/scope-analysis/2024-07-03_fast_scope/set2_cav2.csv")
    rename_df_set2_cav2 = df_set2_cav2.rename(columns={"time": "time_set2_cav2", "values": "values_set2_cav2"})
    clean_df_set2_cav2 = rename_df_set2_cav2.loc[0:len(rename_df_set2_cav2["time_set2_cav2"]),
                                                 "time_set2_cav2": "values_set2_cav2"]

    result_df = pd.concat([clean_df_set2_cav1, clean_df_set2_cav2], axis=1)

    for i in range(3, 13):
        curr_df_cav1 = clean_df(
            f"/Users/jonathontordilla/Desktop/hombom24/scope-analysis/2024-07-03_fast_scope/set{i}_cav1.csv")
        curr_df_cav2 = clean_df(
            f"/Users/jonathontordilla/Desktop/hombom24/scope-analysis/2024-07-03_fast_scope/set{i}_cav2.csv")

        rename_cav1 = curr_df_cav1.rename(columns={"time": f"time_set{i}_cav1", "values": f"values_set{i}_cav1"})
        clean_cav1 = rename_cav1.loc[0:len(rename_cav1[f"time_set{i}_cav1"]),
                                     f"time_set{i}_cav1": f"values_set{i}_cav1"]
        rename_cav2 = curr_df_cav2.rename(columns={"time": f"time_set{i}_cav2", "values": f"values_set{i}_cav2"})
        clean_cav2 = rename_cav2.loc[0:len(rename_cav2[f"time_set{i}_cav2"]),
                                     f"time_set{i}_cav2": f"values_set{i}_cav2"]

        result_df[f"time_set{i}_cav1"] = clean_cav1[f"time_set{i}_cav1"]
        result_df[f"values_set{i}_cav1"] = clean_cav1[f"values_set{i}_cav1"]
        result_df[f"time_set{i}_cav2"] = clean_cav2[f"time_set{i}_cav2"]
        result_df[f"values_set{i}_cav2"] = clean_cav2[f"values_set{i}_cav2"]

    return result_df


def avg_powers(df: pd.DataFrame) -> dict[str, float]:
    """Calculate the average power of the amplitude values in the dataframe.

    https://pysdr.org/content/sampling.html#calculating-power-spectral-density.
    """
    result = {}
    for i in range(2, 13):
        # average power: get the mean of the sequence of the absolute value squared
        result[f"set{i}_cav1"] = float(np.mean(np.abs(df[f"values_set{i}_cav1"].astype(float))**2))
        result[f"set{i}_cav2"] = float(np.mean(np.abs(df[f"values_set{i}_cav2"].astype(float))**2))
    return result


def plot_psd(df: pd.DataFrame, column: str, fs: int = 25e9, fig_width: int = 10, fig_height: int = 7,
             x_label_font_size: int = 14, y_label_font_size: int = 14, title_font_size: int = 16) -> pd.DataFrame:
    """Calculate and plot the power spectrum of the amplitude values in the dataframe.

    Is 25e9 the correct sampling frequency?
    """
    x = df[column].astype("float")
    n = 50000
    psd = np.abs(np.fft.fft(x)) ** 2 / (n * fs)
    psd_log = 10.0 * np.log10(psd)
    psd_shifted = np.fft.fftshift(psd_log)
    center_freq = 0
    f = np.arange(fs / -2.0, fs / 2.0, fs / n)  # start, stop, step centered around 0 Hz
    f += center_freq  # now add center frequency

    # plot the spectra
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    set_label = ", ".join(column.split("_")[1:])
    ax.set_title(f"Power Spectral Density: {set_label}", fontsize=title_font_size)
    ax.set_xlabel("Frequency (GHz)", fontsize=x_label_font_size)
    ax.set_ylabel("Power (dB)", fontsize=y_label_font_size)
    ax.plot(f, psd_shifted)

    # TICK PARAMETERS
    x_tick_locs = ax.get_xticks()
    x_tick_labels = [float((tick.get_text().replace('−', '-')).replace(",", "")) for tick in ax.get_xticklabels()]
    x_tick_labels_new = [round(float(x) * 10, 15) for x in x_tick_labels]  # raise or lower to the given power
    ax.xaxis.set_major_locator(ticker.FixedLocator(x_tick_locs))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(x_tick_labels_new))
    ax.tick_params(axis="x", labelsize=x_label_font_size)
    ax.tick_params(axis="y", labelsize=y_label_font_size)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # reduce the amount of ticks for both axes
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.show()
    # return the DataFrame of frequencies
    df_freq = pd.DataFrame(data={"freq": f, "psd_shift": psd_shifted})
    return df_freq


if __name__ == "__main__":
    full_df = create_full_df()  # creates a DataFrame will data for all files in 2024-07-03 folder

    plot_df(full_df, "time_set4_cav2", "values_set4_cav2")  # example: visualize signal over time

    print(f"average powers: {avg_powers(full_df)}")  # print out the average power of each set

    psd_df = plot_psd(full_df, "values_set2_cav1")  # plot the power spectral density of a set, return DataFrame
