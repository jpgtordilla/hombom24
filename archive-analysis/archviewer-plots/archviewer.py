import numpy as np
import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import matplotlib.ticker as ticker
from scipy.signal import find_peaks
import datetime
import re

class ArchViewer: 
    def __init__(self): 
        return

    # DATA CLEANING

    """Returns a df that can be used in the following functions for cleaning"""
    def csv_to_df(self, file_path): 
        return pd.read_csv(file_path)

    """Returns the ratio of normal elements to total cells"""
    """
    def get_non_na_ratio(self, df_name, col_name): 
        tot_len = len(df_name[col_name])
        na_len = tot_len - len(df_name[col_name].dropna())
        return (tot_len - na_len) / tot_len
    """

    """Returns a df with irrelevant (only applies to small time frames) rows removed"""
    def remove_irrelevant_dates(self, df_name): 
        test_timestamp_list = df_name["Timestamp"].tolist()
        date_only_list = [x[0:10] for x in test_timestamp_list] # list with only dates

        date_counts_dict = Counter(date_only_list)
        common_date = date_counts_dict.most_common(1)[0][0] # get the most common date

        # only get rows that have the common date 

        common_date_only_list = [x if x == common_date else None for x in date_only_list]
        none_length = len([x for x in common_date_only_list if x == None])
        filtered_df = df_name.iloc[none_length:, 0:]
        return filtered_df

    """Returns a df with a single column without NA values"""
    def remove_nan_from_col(self, df_name, col_name): 
        new_df = df_name[pd.notna(df_name[col_name])]
        return new_df[["Timestamp", col_name]]

    """Returns a df without the date and hour in the Timestamp and converts into seconds, starting at the first entry in the timestamp column"""
    def remove_date(self, df_name): 
        # find the "zero" date offset
        date_list = df_name["Timestamp"].to_list()
        zero_date = date_list[0]
        offset = self.remove_date_helper(zero_date)

        # create a list of dates in number form
        num_dates = [0]
        for i in range(1, len(date_list)): 
            curr_date_num = self.remove_date_helper(date_list[i])
            num_dates.append(curr_date_num - offset) # compute offset given by the first entry in the Timestamp df column

        result_df = df_name.copy()
        result_df["Timestamp"] = num_dates
        return result_df
        
    def remove_date_helper(self, date): 
        split_zero_date = re.split(r"/|:| ", date) # split date time string by delimiters
        int_dt = [int(float(x)) for x in split_zero_date] # integer components of date for datetime function
        dt = datetime.datetime(int_dt[0], int_dt[1], int_dt[2], int_dt[3], int_dt[4], int_dt[5]) # datetime object for first date
        return dt.timestamp() # gets seconds since the starting time defined for unix timestamp

    # PLOTTING

    """Grid plotter helper function for megaplots"""
    def plot_mega(self, ax, df_name, y_axis_title, i, j, col_ind, start, end): 
        # df_rows = remove_irrelevant_dates(df_name) # remove irrelevant rows

        if col_ind >= len(df_name.columns): # ends execution of for loop if no more columns to render
            return
        
        df_cols = self.remove_nan_from_col(df_name, df_name.columns[col_ind]) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax[i, j].scatter(df_plot.loc[start:end, ["Timestamp"]]["Timestamp"], df_plot.loc[start:end, [df_name.columns[col_ind]]][df_name.columns[col_ind]], s=10)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].xaxis.set_minor_locator(ticker.LinearLocator(0))
        ax[i, j].tick_params(axis='y', which='major', labelsize=8)
        ax[i, j].tick_params(axis='x', which='major', labelsize=8)
        ax[i, j].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax[i, j].set_xlabel("Time (s)")
        ax[i, j].set_ylabel(y_axis_title)
        ax[i, j].set_title(f"{y_axis_title} vs. Time for {df_name.columns[col_ind]}", {'fontsize': 7})

    """Plot of a specific column in a df"""
    def specific_col_plot(self, df_name, col_name, y_axis_title, start, end): 
        fig, ax = plt.subplots(figsize=(12, 4))
        # print(f"Normal element to total ratio: {self.get_non_na_ratio(df_name, col_name)}") # get normal/total ratio
        # df_rows = remove_irrelevant_dates(df_name) # remove irrelevant rows
        df_cols = self.remove_nan_from_col(df_name, col_name) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax.scatter(df_plot.loc[start:end, ["Timestamp"]]["Timestamp"], df_plot.loc[start:end, [col_name]][col_name])

        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(y_axis_title)
        ax.set_title(f"{y_axis_title} vs. Time for {col_name}")

        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

    """Megaplot of all the columns from the df"""
    def megaplot_all_cols(self, df_name, y_axis_title, start, end): 
        # want to create a grid of subplots
        col_len = len(df_name.columns) - 1
        dim = int(np.sqrt(col_len))
        # the following two lines are subject to change with increasing dimension
        fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))
        plt.subplots_adjust(wspace=0.4, hspace=1)
        col_ind = 1 # track index of the columns in the df that will be cleaned in the for loop
        for i in range(0, dim + 1): 
            for j in range(0, dim):
                self.plot_mega(ax, df_name, y_axis_title, i, j, col_ind, start, end)
                col_ind += 1 # keep track of which column is being plotted
        plt.show()

    # FILTERING

    """plot and return dictionary of indices/peak heights for a df, specified columns, specified x range, and peak parameters"""
    def plot_return_peaks(self, df_name, x_col, y_col, y_label, peak_height, peak_dist, x_start, x_end):
        # plot peaks based on parameters
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        plt.subplots_adjust(wspace=0.4, hspace=0.3)
        y = df_name.loc[x_start:x_end, [y_col]][y_col]
        all_peaks, peak_heights = find_peaks(y, height=peak_height, distance=peak_dist)
        ax[0].plot(df_name.loc[x_start:x_end, [x_col]][x_col], y) 
        ax[0].plot(all_peaks, y[all_peaks], "x")
        ax[0].plot(np.zeros_like(y), "--", color="gray")
        # plot only peak points with x axis showing index corresponding to the returned dict
        ax[1].scatter(all_peaks, y[all_peaks])
        # match limits with the first plot
        ax[1].set_xlim(0, len(df_name.loc[x_start:x_end, [x_col]][x_col]))
        ax[1].set_ylim(-max(peak_heights["peak_heights"].tolist())*1.1, max(peak_heights["peak_heights"].tolist())*1.1)
        # set labels
        for i in range(2): 
            ax[i].set_xlabel(x_col)
            ax[i].set_ylabel(y_label)
            ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
            ax[i].set_title(f"{y_label} vs. Time for {y_col}")
        plt.show()
        result = {all_peaks.tolist()[i]: peak_heights["peak_heights"].tolist()[i] for i in range(len(all_peaks))}
        return result
    
    """only return dictionary of indices/peak heights for a df, specified column, specified x range, and peak parameters"""
    def return_peaks(self, df_name, y_col, x_start, x_end, peak_height, peak_dist):
        y = df_name.loc[x_start:x_end, [y_col]][y_col]
        all_peaks, peak_heights = find_peaks(y, height=peak_height, distance=peak_dist)
        result = {all_peaks.tolist()[i]: peak_heights["peak_heights"].tolist()[i] for i in range(len(all_peaks))}
        return result

    # CORRELATIONS

    """Plot of a specific correlation between two specific dataframes and their specified columns"""
    def spec_correl(self, df_x, df_y, df_col_x, df_col_y, start, end): 
        # clean both dfs
        df_plot_x = self.clean_df(df_x, df_col_x)
        df_plot_y = self.clean_df(df_y, df_col_y)
        # plot dfs
        fig, ax = plt.subplots(figsize=(12, 4))
        # print(f"Normal element to total ratio x: {get_non_na_ratio(df_x, df_col_x)}") # get normal/total ratio
        # print(f"Normal element to total ratio y: {get_non_na_ratio(df_y, df_col_y)}") 
        ax.scatter(df_plot_x.loc[start:end, [df_col_x]][df_col_x], df_plot_y.loc[start:end, [df_col_y]][df_col_y]) # must specify indices to plot
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax.set_xlabel(df_col_x)
        ax.set_ylabel(df_col_y)
        ax.set_title(f"{df_col_y} vs. {df_col_x}")
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        plt.show()

    """Plot a correlation between a specific column from a df and all the columns in the other df"""
    def correl(self, df_y, df_y_col, df_x, start, end): 
        # want to create a grid of subplots
        col_len = len(df_x.columns) - 1
        dim = int(np.sqrt(col_len))
        # the following two lines are subject to change with increasing dimension
        fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))
        plt.subplots_adjust(wspace=0.4, hspace=1)
        col_ind = 1 # track index of the columns in the df that will be cleaned in the for loop
        for i in range(0, dim + 1): 
            for j in range(0, dim):
                if col_ind >= len(df_x.columns): 
                    break
                self.plot_correl_mega(ax, df_y, df_y_col, df_x, i, j, col_ind, start, end)

                col_ind += 1 # keep track of which column is being plotted
        plt.show()

    """Helper function to clean df"""
    def clean_df(self, df, col): 
        df_cols = self.remove_nan_from_col(df, col) # df with only the one specified col df_col_x
        return self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

    """Helper function to clean both dfs"""
    def clean_df_both(self, df_1, df_2, col_1, col_2): 
        df1_copy = df_1.copy()
        df2_copy = df_2.copy()
        df1_clean = self.remove_nan_from_col(df1_copy, col_1)
        df2_clean = self.remove_nan_from_col(df2_copy, col_2)   
        # merge only when Timestamp values match
        # citation: https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
        result = pd.merge(df1_clean, df2_clean[["Timestamp", col_2]], on='Timestamp')
        return result

    """Helper function for correlation megaplots"""
    def plot_correl_mega(self, ax, df_y, df_y_col, df_x, i, j, col_ind, start, end): 

        # want to clean both dfs simultaneously, so that only non-NaN rows are maintained

        df_plot = self.clean_df_both(df_y, df_x, df_y_col, df_x.columns[col_ind])

        if df_y_col == df_x.columns[col_ind]: 
            ax[i, j].scatter(df_plot.loc[start:end, [f"{df_y_col}_y"]][f"{df_y_col}_y"], 
                            df_plot.loc[start:end, [f"{df_x.columns[col_ind]}_x"]][f"{df_x.columns[col_ind]}_x"], s=10)
        else: 
            ax[i, j].scatter(df_plot.loc[start:end, [df_y_col]][df_y_col], 
                            df_plot.loc[start:end, [df_x.columns[col_ind]]][df_x.columns[col_ind]], s=10)

        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].xaxis.set_minor_locator(ticker.LinearLocator(0))
        ax[i, j].tick_params(axis='y', which='major', labelsize=8)
        ax[i, j].tick_params(axis='x', which='major', labelsize=8)
        ax[i, j].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax[i, j].set_xlabel(df_x.columns[col_ind])
        ax[i, j].set_ylabel(df_y_col)
        ax[i, j].set_title(f"{df_y_col} vs. {df_x.columns[col_ind]}", {'fontsize': 7})