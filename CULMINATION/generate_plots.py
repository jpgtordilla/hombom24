import charge_separator as cs
from concurrent.futures import ThreadPoolExecutor
import charge_plotter as cp
import pandas as pd
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import archiver_data_process as ap  # type: ignore


def get_pairs_of_dates(file_path):
    """Gets all 10 minute time intervals before the dates listed in the LCLS-II logbook."""
    # read the html file locally
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # use beautiful soup to parse the html file
    soup = BeautifulSoup(html_content, 'html.parser')
    dates = []
    times = []

    # search by class name: header_date gives the day of log
    date_tags = soup.find_all(class_='header_date')
    for tag in date_tags:
        curr_date = tag.get_text(strip=True)
        dates.append(curr_date)

    # header_time gives the time of the day at which the buncher phase scan was performed
    time_tags = soup.find_all(class_='header_time')
    for tag in time_tags:
        curr_time = tag.get_text(strip=True)
        times.append(curr_time)

    # Create a list of datetimes of all the entries in the logbook
    datetimes = []
    for index in range(len(dates)):
        datetimes.append(f"{dates[index]} {times[index]}")

    # Create list pairs of datetimes so that they can be accessed later to indicate plotting time ranges
    date_lists = [
        [(datetime.strptime(datetimes[i], "%m/%d/%Y %H:%M") -
          timedelta(minutes=PHASE_TIME_RANGE)).strftime("%Y/%m/%d %H:%M:%S"),
         datetime.strptime(datetimes[i], "%m/%d/%Y %H:%M").strftime("%Y/%m/%d %H:%M:%S")] for i in
        range(len(datetimes))]

    return date_lists


def filter_hom(df_hom: pd.DataFrame) -> pd.DataFrame:
    return df_hom[(df_hom[PV_HOM] > -0.2) & (df_hom[PV_HOM] < 0)]


def plot_buncher_phase_scan_all(date_list, pv_list, label_list, unit_list):
    """Plots buncher phase scan over time, then combined correlations with HOM vs. other PVs over a long timeframe."""
    # COMBINE TIMEFRAMES AND FIND CORRELATIONS
    correl_homc1_cor_list = []
    correl_homc1_bpm_list = []

    # correlation list for charge correlation
    correl_homc1_charge_list = []

    # only iterate through the desired buncher phase scans
    start_index_inclusive = len(date_list) - END_SCAN
    end_index_exclusive = start_index_inclusive + (END_SCAN - START_SCAN) + 1
    for x in range(start_index_inclusive, end_index_exclusive):
        curr_start_date = date_list[x][0]
        curr_end_date = date_list[x][1]

        # create DataFrames
        df_cor = arch_plotter.create_df(arch_plotter.pv(pv_list[0], curr_start_date, curr_end_date))
        df_bpm = arch_plotter.create_df(arch_plotter.pv(pv_list[1], curr_start_date, curr_end_date))
        df_hom = arch_plotter.create_df(arch_plotter.pv(pv_list[2], curr_start_date, curr_end_date))
        df_hom_filter = filter_hom(df_hom)
        df_charge = arch_plotter.create_df(arch_plotter.pv(pv_list[3], curr_start_date, curr_end_date))

        # create correlations and add to list
        df_charge_filtered = plotter.remove_charges_below_value(df_charge, pv_list[-1], 15.0)
        df_charge_cor = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_cor,
                                                               time_margin_seconds=TIME_MARGIN_SECONDS)
        df_charge_bpm = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_bpm,
                                                               time_margin_seconds=TIME_MARGIN_SECONDS)
        df_correl_homc1_cor = plotter.merge_with_margin_on_timestamp(df_charge_cor, df_hom_filter,
                                                                     time_margin_seconds=TIME_MARGIN_SECONDS)
        df_correl_homc1_bpm = plotter.merge_with_margin_on_timestamp(df_charge_bpm, df_hom_filter,
                                                                     time_margin_seconds=TIME_MARGIN_SECONDS)

        # create correlation for charge plot
        df_correl_charge_homc1 = plotter.merge_with_margin_on_timestamp(df_charge, df_hom_filter,
                                                                        time_margin_seconds=TIME_MARGIN_SECONDS)

        correl_homc1_cor_list.append(df_correl_homc1_cor)
        correl_homc1_bpm_list.append(df_correl_homc1_bpm)

        correl_homc1_charge_list.append(df_correl_charge_homc1)

    # combine dataframes from list and sort
    df_correl_homc1_cor = pd.concat(correl_homc1_cor_list).sort_values(by=["Timestamp"])
    df_correl_homc1_bpm = pd.concat(correl_homc1_bpm_list).sort_values(by=["Timestamp"])

    # plot HOM vs. X/YCOR
    plotter.plot_correlation(df_correl_homc1_cor,
                             pv_y=pv_list[2],
                             pv_x=pv_list[0],
                             pv_charge=pv_list[-1],
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=pv_list[0],
                             error_tolerance=0.000015,
                             x_label=label_list[0],
                             y_label=label_list[2],
                             x_units=unit_list[0],
                             y_units=unit_list[2],
                             x_change_decimal_point=3,
                             same_day=True)

    # plot HOM vs. BPM X/Y
    plotter.plot_correlation(df_correl_homc1_bpm,
                             pv_y=pv_list[2],
                             pv_x=pv_list[1],
                             pv_charge=pv_list[-1],
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=pv_list[1],
                             error_tolerance=0.000015,
                             x_label=label_list[1],
                             y_label=label_list[2],
                             x_units=unit_list[1],
                             y_units=unit_list[2],
                             x_change_decimal_point=0,
                             same_day=True)


def plot_xcor_long(xlabel, ylabel, xunits, yunits):
    """HOM VS. XCOR, over a long period."""
    df_xcor = arch_plotter.create_df(arch_plotter.pv(PV_XCOR, START_TIME, END_TIME))
    df_chrg_xcor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_xcor,
                                                          time_margin_seconds=TIME_MARGIN_SECONDS)
    df_correl_chrg_xcor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_xcor, df_homc1,
                                                                       time_margin_seconds=TIME_MARGIN_SECONDS)
    plotter.plot_correlation(df_correl_chrg_xcor_homc1,
                             pv_y=PV_HOM,
                             pv_x=PV_XCOR,
                             pv_charge=PV_CHARGE,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=PV_XCOR,
                             error_tolerance=0.000015,
                             x_label=xlabel,
                             y_label=ylabel,
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units=xunits,
                             y_units=yunits,
                             x_change_decimal_point=3)


def plot_ycor_long(xlabel, ylabel, xunits, yunits):
    """HOM VS. YCOR, over a long period."""
    df_ycor = arch_plotter.create_df(arch_plotter.pv(PV_YCOR, START_TIME, END_TIME))
    df_chrg_ycor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_ycor,
                                                          time_margin_seconds=TIME_MARGIN_SECONDS)
    df_correl_chrg_ycor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_ycor, df_homc1,
                                                                       time_margin_seconds=TIME_MARGIN_SECONDS)
    plotter.plot_correlation(df_correl_chrg_ycor_homc1,
                             pv_y=PV_HOM,
                             pv_x=PV_YCOR,
                             pv_charge=PV_CHARGE,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=PV_YCOR,
                             error_tolerance=0.000015,
                             x_label=xlabel,
                             y_label=ylabel,
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units=xunits,
                             y_units=yunits,
                             x_change_decimal_point=3)


def plot_bpmx_long(xlabel, ylabel, xunits, yunits):
    """HOM VS. BPMX, over a long period."""
    df_bpmx = arch_plotter.create_df(arch_plotter.pv(PV_BPMX, START_TIME, END_TIME))
    df_chrg_bpmx = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmx,
                                                          time_margin_seconds=TIME_MARGIN_SECONDS)
    df_correl_chrg_bpmx_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmx, df_homc1,
                                                                       time_margin_seconds=TIME_MARGIN_SECONDS)
    plotter.plot_correlation(df_correl_chrg_bpmx_homc1,
                             pv_y=PV_HOM,
                             pv_x=PV_BPMX,
                             pv_charge=PV_CHARGE,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=PV_BPMX,
                             error_tolerance=0.000015,
                             x_label=xlabel,
                             y_label=ylabel,
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units=xunits,
                             y_units=yunits,
                             x_change_decimal_point=0)


def plot_bpmy_long(xlabel, ylabel, xunits, yunits):
    """HOM VS. BPMY, over a long period."""
    df_bpmy = arch_plotter.create_df(arch_plotter.pv(PV_BPMY, START_TIME, END_TIME))
    df_chrg_bpmy = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmy,
                                                          time_margin_seconds=TIME_MARGIN_SECONDS)
    df_correl_chrg_bpmy_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmy, df_homc1,
                                                                       time_margin_seconds=TIME_MARGIN_SECONDS)
    plotter.plot_correlation(df_correl_chrg_bpmy_homc1,
                             pv_y=PV_HOM,
                             pv_x=PV_BPMY,
                             pv_charge=PV_CHARGE,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=CHARGE_TOLERANCE,
                             plot_error_bars=False,
                             low_vary_column=PV_BPMY,
                             error_tolerance=0.000015,
                             x_label=xlabel,
                             y_label=ylabel,
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units=xunits,
                             y_units=yunits,
                             x_change_decimal_point=0)


def plot_xcor_bpmx_phase(labels, units):
    """HOM VS. XCOR, BPM X for XCOR/BPMX Buncher Phase Scan."""
    pvs_xcor_bpmx_phase = [PV_XCOR, PV_BPMX, PV_HOM, PV_CHARGE]
    labels_xcor_bpmx_phase = labels
    units_xcor_bpmx_phase = units
    plot_buncher_phase_scan_all(START_END_DATES, pvs_xcor_bpmx_phase, labels_xcor_bpmx_phase, units_xcor_bpmx_phase)


def plot_ycor_bpmy_phase(labels, units):
    """HOM VS. YCOR, BPM Y for XCOR/BPMX Buncher Phase Scan."""
    pvs_ycor_bpmy_phase = [PV_YCOR, PV_BPMY, PV_HOM, PV_CHARGE]
    labels_ycor_bpmy_phase = labels
    units_ycor_bpmy_phase = units
    plot_buncher_phase_scan_all(START_END_DATES, pvs_ycor_bpmy_phase, labels_ycor_bpmy_phase, units_ycor_bpmy_phase)


if __name__ == '__main__':
    plotter = cp.ChargePlotter()
    arch_plotter = ap

    # PARAMETERS: set before generating plots
    PV_HOM = "SCOP:AMRF:RF01:AI_MEAS1"
    PV_XCOR = "XCOR:GUNB:713:BACT"  # XCOR 04
    PV_BPMX = "BPMS:GUNB:925:X"  # BPMX 02
    PV_YCOR = "YCOR:GUNB:713:BACT"  # YCOR 04
    PV_BPMY = "BPMS:GUNB:925:Y"  # BPMY 02
    PV_CHARGE = "TORO:GUNB:360:CHRG"
    START_TIME = "2024/03/21 00:00:00"
    END_TIME = "2024/04/02 23:59:59"
    MIN_CHARGE_VAL = 15.0  # minimum charge to include in the DataFrame of charges
    CHARGE_VAL = 50.0  # set this to separate out by charge (pC), all values are: 50, 60, 80, 100, 140
    CHARGE_TOLERANCE = 0.1  # groups charges together within 10%, can set anywhere between 0-1
    TIME_MARGIN_SECONDS = 0.5  # amount of seconds between timestamps on which to merge DataFrames
    PHASE_TIME_RANGE = 10  # amount of minutes before the LCLS-II logbook date for the buncher phase scan (around 10m)
    START_SCAN = 1  # which buncher phase scan to start assembling plots from, in chronological order
    END_SCAN = 10  # which buncher phase scan to end assembling plots from, inclusive
    # change to your path to the HTML file for the LCLS-II logbook, search keyword: "Corrector XC04"
    START_END_DATES = get_pairs_of_dates("/Users/jonathontordilla/Desktop/hombom24/CULMINATION/buncher_dates.html")

    # DataFrames needed for every plot: HOM C1 and CHARGE
    df_homc1 = arch_plotter.create_df(arch_plotter.pv(PV_HOM, START_TIME, END_TIME))
    df_homc1 = filter_hom(df_homc1)
    df_chrg = arch_plotter.create_df(arch_plotter.pv(PV_CHARGE, START_TIME, END_TIME))
    df_chrg_filtered = plotter.remove_charges_below_value(df_chrg, PV_CHARGE, min_charge_value=MIN_CHARGE_VAL)

    df_charge_homc1 = arch_plotter.merge_dfs_with_margin_by_timestamp_column(df_chrg_filtered, df_homc1,
                                                                             time_margin_seconds=TIME_MARGIN_SECONDS)

    # GENERATE PLOTS
    plot_functions = [
        plot_xcor_long("XCOR 04 Magnet", "HOM C1 Signal", "(G*m)", "(arb. units)"),
        plot_ycor_long("YCOR 04 Magnet", "HOM C1 Signal", "(G*m)", "(arb. units)"),
        plot_bpmx_long("BPM 02 X", "HOM C1 Signal", "(mm)", "(arb. units)"),
        plot_bpmy_long("BPM 02 Y", "HOM C1 Signal", "(mm)", "(arb. units)"),
        plot_xcor_bpmx_phase(["XCOR 04 Magnet", "BPM 02 X", "HOM C1 Signal", "Charge"],
                             ["(G*m)", "(mm)", "(arbitrary units)"]),
        plot_ycor_bpmy_phase(["YCOR 04 Magnet", "BPM 02 Y", "HOM C1 Signal", "Charge"],
                             ["(G*m)", "(mm)", "(arbitrary units)"])
    ]
    # https://docs.python.org/3/library/concurrent.futures.html
    with ThreadPoolExecutor() as executor:
        executor.map(lambda f: f(), plot_functions)  # high level asynchronous call to avoid timeouts

