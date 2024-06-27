import numpy as np
import pandas as pd # type: ignore
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import matplotlib.ticker as ticker

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

    """Returns a df with irrelevant rows removed"""
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

    """Returns a df without the date and hour in the Timestamp"""
    def remove_date(self, df_name): 
        timestamps = df_name["Timestamp"]
        result_timestamps = [x[14:] for x in timestamps]
        result_df = df_name.copy()
        result_df["Timestamp"] = result_timestamps
        return result_df

    # PLOTTING

    """Grid plotter helper function for megaplots"""
    def plot_mega(self, ax, df_name, y_axis_title, i, j, col_ind): 
        df_rows = self.remove_irrelevant_dates(df_name) # remove irrelevant rows

        if col_ind >= len(df_rows.columns): # ends execution of for loop if no more columns to render
            return
        
        df_cols = self.remove_nan_from_col(df_rows, df_rows.columns[col_ind]) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax[i, j].scatter(df_plot["Timestamp"], df_plot[df_rows.columns[col_ind]], s=10)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].xaxis.set_minor_locator(ticker.LinearLocator(0))
        ax[i, j].tick_params(axis='y', which='major', labelsize=8)
        ax[i, j].tick_params(axis='x', which='major', labelsize=8)
        ax[i, j].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax[i, j].set_xlabel("Time (min:sec)")
        ax[i, j].set_ylabel(y_axis_title)
        ax[i, j].set_title(f"{y_axis_title} vs. Time for {df_rows.columns[col_ind]}", {'fontsize': 7})

    """Plot of a specific column in a df"""
    def specific_col_plot(self, df_name, col_name, y_axis_title): 
        fig, ax = plt.subplots(figsize=(12, 4))
        print(f"Normal element to total ratio: {self.get_non_na_ratio(df_name, col_name)}") # get normal/total ratio
        df_rows = self.remove_irrelevant_dates(df_name) # remove irrelevant rows
        df_cols = self.remove_nan_from_col(df_rows, col_name) # remove unwanted columns
        df_plot = self.remove_date(df_cols) # modify timestamp text to only include the hour, min, and sec

        ax.scatter(df_plot["Timestamp"], df_plot[col_name])

        # x label is always in seconds, but y label must be specified by the user as it is not given in the csv file
        ax.set_xlabel("Time (min:sec)")
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
        