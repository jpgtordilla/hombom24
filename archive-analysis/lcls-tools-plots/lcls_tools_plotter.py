import sys
sys.path.append('/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools') # change to your path to lcls_tools
import common.data_analysis.archiver as arch # type: ignore
from datetime import datetime
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import find_peaks

class LclsToolsPlotter(): 
    def __init__(self): 
        return
    
    """Create and return a DataFrame given a PV and start/end date"""
    """Example: create_df('SOLN:GUNB:100:BACT', '2024/07/02 14:42:36', '2024/07/02 15:42:36')"""
    def create_df(self, pv_str: str, start: str, end: str): 
        # specify a start and end date
        format_string = "%Y/%m/%d %H:%M:%S"
        start_date_obj = datetime.strptime(start, format_string) # create a datetime object
        end_date_obj = datetime.strptime(end, format_string)
        # submit request with a list of PVs
        data = arch.get_values_over_time_range([pv_str], start_date_obj, end_date_obj)
        # create a dictionary for a PV, access it with timestamps and values methods from archiver.py
        pv_dict = data[pv_str]
        pv_timestamps = pv_dict.timestamps
        pv_values = pv_dict.values
        pv_clean_timestamps = [pv_timestamps[i].strftime('%m/%d/%Y %H:%M:%S') for i in range(len(pv_timestamps))] # clean and reformat timestamps from the dict
        return pd.DataFrame({"timestamps": pv_clean_timestamps, pv_str: pv_values}) # create df with columns
    
    """Plots a nonempty list of PVs over time"""
    def plot_pv_over_time(self, pv_list: list, start: str, end: str): 
        fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
        if len(pv_list) > 0: 
            for pv_str in pv_list: 
                df = self.create_df(pv_str, start, end)
                ax.scatter(df["timestamps"], df[pv_str], label=pv_str)
                ax.set_xlabel("Timestamp")
            ax.xaxis.set_major_locator(ticker.LinearLocator(5))
            ax.set_title("PVs vs. Time") 
            ax.legend() 
            plt.show()
        else: 
            return "Could not plot PVs because an empty list was given"
        
    """Create a megaplot of PVs with respect to time"""
    def megaplot_pvs_over_time(self, pv_list: list, start: str, end: str, w_margin=0.4, h_margin=1): 
        if len(pv_list) < 1: 
            return IndexError("Could not plot PVs because an empty list was given")
        # if the length of pv_list is only 1, call the single plot function 
        if len(pv_list) == 1: 
            self.plot_pv_over_time([pv_list[0]], start, end)
            return
        # want to create a grid of subplots
        col_len = len(pv_list)
        dim = int(np.round(np.sqrt(col_len))) # dimension of the grid

        # IF DIMENSION < 2: create two subplots side by side
        if dim < 2: 
            fig, (ax0, ax1) = plt.subplots(1, 2)
            fig.suptitle("PVs vs. Time")
            # generate dfs and axes for each pv
            for i in range(2): 
                pv_str = pv_list[i]
                curr_ax = fig.get_axes()[i]
                df = self.create_df(pv_str, start, end)
                curr_ax.scatter(df["timestamps"], df[pv_str], label=pv_str)
                curr_ax.set_xlabel("Timestamp", fontsize=10)
                curr_ax.xaxis.set_major_locator(ticker.LinearLocator(3))
                curr_ax.set_xticklabels(df["timestamps"], fontsize=5)
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin)

        # IF DIMENSION >= 2: create a grid of subplots that are indexed in a loop 
        else: 
            fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15)) # add an extra row to account for rounding 
            plt.subplots_adjust(wspace=w_margin, hspace=h_margin) # can set if needed using optional parameters
            df_ind = 0 # track index of the which df is being plotted

            # create a list of DataFrames for each pv in pv_list
            df_list = [self.create_df(pv_list[i], start, end) for i in range(len(pv_list))]
            
            # iterate through the grid 
            for i in range(0, dim + 1): # for every row in the grid
                for j in range(0, dim): # for every column in the grid
                    if df_ind >= len(df_list): 
                        break
                    self.plot_mega(ax, df_list[df_ind], i, j, df_ind)
                    df_ind += 1 # go to the next df in the list
        plt.show()
        return 
    
    """Grid plotter helper function for megaplots"""
    def plot_mega(self, ax, df_name, i: int, j: int, df_ind: int): 
        ax[i, j].scatter(df_name["timestamps"], df_name[df_name.columns[1]], s=10)
        ax[i, j].xaxis.set_major_locator(ticker.LinearLocator(3))
        ax[i, j].set_xlabel("Timestamp")
        ax[i, j].set_title(f"PV vs. Time for {df_name.columns[1]}", {'fontsize': 10})

    """Return peaks for a list of PVs as a 2D dictionary (similar to a JSON file)"""
    def return_peaks(self, pv_list: list, start: str, end: str, peak_height: float, peak_spacing: float): 
        if len(pv_list) < 1: 
            return IndexError("Could not plot PVs because an empty list was given")
        result_dict = {} # 2D dictionary, keys for each pv, with keys for each peak index and its height
        for pv_name in pv_list: 
            df_curr = self.create_df(pv_name, start, end)
            y_axis = df_curr[pv_name] # get the column that corresponds with the pv values
            all_peaks, peak_heights = find_peaks(y_axis, height=peak_height, distance=peak_spacing) # use scipy to generate lists of peak indices and their heights
            result = {all_peaks.tolist()[i]: peak_heights["peak_heights"].tolist()[i] for i in range(len(all_peaks))}
            result_dict[pv_name] = result # add to 2D dictionary
        return result_dict
    
    """Plot peaks on a PV graph as well as the individual data points and return the 2D dictionary"""
    """If is_correl is set to True, then it plots the correlation between the second item in the list vs. the first item: [x, y]"""
    def plot_return_peaks(self, pv_list: list, start: str, end: str, peak_height: float, peak_spacing: float, is_correl=False): 
        # plot peaks based on parameters
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        plt.subplots_adjust(wspace=0.4, hspace=0.3)

        # IF PLOTTING A CORRELATION
        if is_correl: 
            df_curr = self.create_correlation_df(pv_list[0], pv_list[1], start, end)
            y = df_curr[pv_list[1]]
            x = df_curr[pv_list[0]]
            all_peaks, peak_heights = find_peaks(y, height=peak_height, distance=peak_spacing) # use scipy to generate lists of peak indices and their heights
            ax[0].scatter(df_curr[pv_list[0]], df_curr[pv_list[1]]) 

            # plot only peak points with x axis showing index corresponding to the returned dict
            ax[1].scatter(all_peaks, y[all_peaks])
            # match limits (approximately) with the first plot
            ax[1].set_xlim(0, len(x))

            # set labels
            for i in range(2): 
                ax[i].set_xlabel(f"{pv_list[0]}")
                ax[i].set_ylabel(f"{pv_list[1]}")
                ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
                ax[i].yaxis.set_major_locator(ticker.LinearLocator(5))
                # set significant figures
                x_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in x] # convert to scientific notation
                y_ticks = [np.format_float_scientific(i, precision=3, min_digits=2) for i in y]
                ax[i].set_xticklabels(x_ticks, fontsize=10) # set tick labels
                ax[i].set_yticklabels(y_ticks, fontsize=10) # set tick labels
                ax[i].set_title(f"{pv_list[1]} vs. {pv_list[0]}")
        
        # IF PLOTTING A TIMESERIES
        else:  
            for pv_name in pv_list: 
                df_curr = self.create_df(pv_name, start, end)
                y = df_curr[pv_name]
                all_peaks, peak_heights = find_peaks(y, height=peak_height, distance=peak_spacing) # use scipy to generate lists of peak indices and their heights
                ax[0].scatter(df_curr["timestamps"], y) 
                ax[0].plot(all_peaks, y[all_peaks], "x", color="red")
                ax[0].plot(np.zeros_like(y), "--", color="gray")
                # plot only peak points with x axis showing index corresponding to the returned dict
                ax[1].scatter(all_peaks, y[all_peaks])
                # match limits (approximately) with the first plot
                ax[1].set_xlim(0, len(df_curr["timestamps"]))
            ax[0].legend() 
                
            # set labels
            for i in range(2): 
                ax[i].set_xlabel("Timestamp")
                ax[i].xaxis.set_major_locator(ticker.LinearLocator(5))
                ax[i].set_xticklabels(df_curr["timestamps"], fontsize=10) # set tick labels
                ax[i].set_title(f"PV vs. Time")
        
        plt.show()
        return self.return_peaks(pv_list, start, end, peak_height, peak_spacing)
    
    """Given two PVs, return a single DataFrame with matching and aligned timestamps"""
    def create_correlation_df(self, pv_one, pv_two, start, end): 
        df_one = self.create_df(pv_one, start, end)
        df_two = self.create_df(pv_two, start, end)
        return pd.merge(df_one, df_two, on="timestamps") # merge DataFrames on equal timestamp strings
    
    """Plot the correlation of pv_two vs. pv_one"""
    def plot_correlation(self, pv_one: str, pv_two: str, start: str, end: str): 
        fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
        df = self.create_correlation_df(pv_one, pv_two, start, end)
        ax.scatter(df[pv_one], df[pv_two], label=f"{pv_two} vs. {pv_one}")
        ax.set_xlabel(f"{pv_one}")
        ax.set_ylabel(f"{pv_two}")
        ax.xaxis.set_major_locator(ticker.LinearLocator(5))
        ax.set_title(f"{pv_two} vs. {pv_one}") 
        ax.legend() 
        plt.show()

    """Megaplot of correlation between a PV and a list of PVs"""
    def megaplot_correlation(self, pv_y: str, pv_list: str, start: str, end: str): 
        pass

# TODO: 
# High Priority
# - megaplot a correlation between a PV and a list of PVs
# - charge and magnet plots
# - HOM plots... 
# Low Priority
# - get units for a specific PV
# - add axis labels for method "plot_pv_over_time"
# - enable correlation peak finding (pick columns with calling scatter with an index instead of by name)
# - determine how the following two lines are subject to change with increasing dimension (megaplot_pvs_over_time)
    # fig, ax = plt.subplots(dim + 1, dim, figsize=(17, 15))
    # plt.subplots_adjust(wspace=0.4, hspace=1)
# - plot peaks with the same xlim and ylim of the original graph


