import numpy as np
import pandas as pd # type: ignore
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import matplotlib.ticker as ticker
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
    def get_non_na_ratio(self, df_name, col_name): 
        tot_len = len(df_name[col_name])
        na_len = tot_len - len(df_name[col_name].dropna())
        return (tot_len - na_len) / tot_len

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
    def plot_mega(self, ax, df_name, y_axis_title, i, j, col_ind): 
        # df_rows = self.remove_irrelevant_dates(df_name) # remove irrelevant rows

        if col_ind >= len(df_name.columns): # ends execution of for loop if no more columns to render
            return
        
        df_cols = self.remove_nan_from_col(df_name, df_name.columns[col_ind]) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax[i, j].scatter(df_plot["Timestamp"], df_plot[df_name.columns[col_ind]], s=10)
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
    def specific_col_plot(self, df_name, col_name, y_axis_title): 
        fig, ax = plt.subplots(figsize=(12, 4))
        print(f"Normal element to total ratio: {self.get_non_na_ratio(df_name, col_name)}") # get normal/total ratio
        # df_rows = self.remove_irrelevant_dates(df_name) # remove irrelevant rows
        df_cols = self.remove_nan_from_col(df_name, col_name) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax.scatter(df_plot["Timestamp"], df_plot[col_name])

        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(y_axis_title)
        ax.set_title(f"{y_axis_title} vs. Time for {col_name}")
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        plt.show()

    """Megaplot of all the columns from the df"""
    def megaplot_all_cols(self, df_name, y_axis_title): 
        # want to create a grid of subplots
        col_len = len(df_name.columns) - 1
        dim = int(np.sqrt(col_len))
        # the following two lines are subject to change with increasing dimension
        fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))
        plt.subplots_adjust(wspace=0.4, hspace=1)
        col_ind = 1 # track index of the columns in the df that will be cleaned in the for loop
        for i in range(0, dim + 1): 
            for j in range(0, dim):
                self.plot_mega(ax, df_name, y_axis_title, i, j, col_ind)
                col_ind += 1 # keep track of which column is being plotted

        plt.show()

    # CORRELATIONS

    """Plot of a specific correlation between two specific dataframes and their specified columns"""
    def spec_correl(self, df_x, df_y, df_col_x, df_col_y): 
        # clean both dfs
        df_plot_x = self.clean_df(df_x, df_col_x)
        df_plot_y = self.clean_df(df_y, df_col_y)
        # plot dfs
        fig, ax = plt.subplots(figsize=(12, 4))
        print(f"Normal element to total ratio x: {self.get_non_na_ratio(df_x, df_col_x)}") # get normal/total ratio
        print(f"Normal element to total ratio y: {self.get_non_na_ratio(df_y, df_col_y)}") 
        ax.scatter(df_plot_x[df_col_x], df_plot_y[df_col_y])
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax.set_xlabel(df_col_x)
        ax.set_ylabel(df_col_y)
        ax.set_title(f"{df_col_y} vs. {df_col_x}")
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        plt.show()

    """Helper function to clean df for correlation function"""
    def clean_df(self, df, col): 
        df_rows = self.remove_irrelevant_dates(df) # remove irrelevant rows 
        df_cols = self.remove_nan_from_col(df_rows, col) # df with only the one specified col df_col_x
        return self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec
    
    """Plot a correlation between a specific column from a df and all the columns in the other df
        if is_x is true, df_y is plotted on y-axis and all columns from df_x are plotted"""
    def correl(self, df_y, df_y_col, df_x, df_x_col, is_x): 
        # want to create a grid of subplots
        col_len = len(df_x.columns) - 1
        dim = int(np.sqrt(col_len))
        # the following two lines are subject to change with increasing dimension
        fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))
        plt.subplots_adjust(wspace=0.4, hspace=1)
        col_ind = 1 # track index of the columns in the df that will be cleaned in the for loop
        for i in range(0, dim + 1): 
            for j in range(0, dim):
                if is_x: # if this is true, df_y is plotted on y-axis and all columns from df_x are plotted
                    self.plot_correl_mega(ax, df_y, df_y_col, df_x, i, j, col_ind)
                else: # if this is true, df_x is plotted on y-axis and all columns from df_y are plotted
                    self.plot_correl_mega(ax, df_x, df_x_col, df_y, i, j, col_ind)

                col_ind += 1 # keep track of which column is being plotted


    """Helper function for correlation megaplots"""
    def plot_correl_mega(self, ax, df_y, df_y_col, df_x, i, j, col_ind): 
        # df_rows = remove_irrelevant_dates(df_name) # remove irrelevant rows

        if col_ind >= len(df_x.columns): # ends execution of for loop if no more columns to render
            return
        
        df_cols = self.remove_nan_from_col(df_x, df_x.columns[col_ind]) # remove unwanted columns and keep the specified one
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        # plots are only generated if the x and y axis have the same amount of points
        if len(df_y[df_y_col]) != len(df_plot[df_x.columns[col_ind]]): 
            return
        
        ax[i, j].scatter(df_y[df_y_col], df_plot[df_x.columns[col_ind]], s=10)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].xaxis.set_minor_locator(ticker.LinearLocator(0))
        ax[i, j].tick_params(axis='y', which='major', labelsize=8)
        ax[i, j].tick_params(axis='x', which='major', labelsize=8)
        ax[i, j].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax[i, j].set_xlabel(df_x.columns[col_ind])
        ax[i, j].set_ylabel(df_y_col)
        ax[i, j].set_title(f"{df_y_col} vs. {df_x.columns[col_ind]}", {'fontsize': 7})
            