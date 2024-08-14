import charge_separator as cs
import charge_plotter as cp
import pandas as pd
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import archiver_data_process as ap  # type: ignore

pv_hom = "SCOP:AMRF:RF01:AI_MEAS1"
pv_xcor = "XCOR:GUNB:713:BACT"  # XCOR 04
pv_bpmx = "BPMS:GUNB:925:X"  # BPMX 02
pv_ycor = "YCOR:GUNB:713:BACT"  # YCOR 04
pv_bpmy = "BPMS:GUNB:925:Y"  # BPMY 02
pv_charge = "TORO:GUNB:360:CHRG"


def get_pairs_of_dates(file_path):
    """Gets all 10 minute time intervals before the dates listed in the LCLS-II logbook"""
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
        [(datetime.strptime(datetimes[i], "%m/%d/%Y %H:%M") - timedelta(minutes=10)).strftime("%Y/%m/%d %H:%M:%S"),
         datetime.strptime(datetimes[i], "%m/%d/%Y %H:%M").strftime("%Y/%m/%d %H:%M:%S")] for i in
        range(len(datetimes))]

    return date_lists


start_end_dates = get_pairs_of_dates("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/"
                                     "charge_separated_plots/buncher_dates.html")


def filter_hom(df_hom: pd.DataFrame) -> pd.DataFrame:
    return df_hom[(df_hom["SCOP:AMRF:RF01:AI_MEAS1"] > -0.2) & (df_hom["SCOP:AMRF:RF01:AI_MEAS1"] < 0)]


def plot_over_time_and_correlation(date_list, pv_list, label_list, unit_list):
    # COMBINE TIMEFRAMES AND FIND CORRELATIONS
    correl_homc1_cor_list = []
    correl_homc1_bpm_list = []

    # correlation list for charge correlation
    correl_homc1_charge_list = []

    for x in range(len(start_end_dates)):  # all times from the bunches_dates.html file
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
        df_charge_cor = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_cor, time_margin_seconds=1.5)
        df_charge_bpm = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_bpm, time_margin_seconds=1.5)
        df_correl_homc1_cor = plotter.merge_with_margin_on_timestamp(df_charge_cor, df_hom_filter,
                                                                     time_margin_seconds=1.5)
        df_correl_homc1_bpm = plotter.merge_with_margin_on_timestamp(df_charge_bpm, df_hom_filter,
                                                                     time_margin_seconds=1.5)

        # create correlation for charge plot
        df_correl_charge_homc1 = plotter.merge_with_margin_on_timestamp(df_charge, df_hom_filter,
                                                                        time_margin_seconds=1.5)

        correl_homc1_cor_list.append(df_correl_homc1_cor)
        correl_homc1_bpm_list.append(df_correl_homc1_bpm)

        correl_homc1_charge_list.append(df_correl_charge_homc1)

    # combine dataframes from list and sort
    df_correl_homc1_cor = pd.concat(correl_homc1_cor_list).sort_values(by=["Timestamp"])
    df_correl_homc1_bpm = pd.concat(correl_homc1_bpm_list).sort_values(by=["Timestamp"])

    # charge correlation
    df_correl_charge_homc1 = pd.concat(correl_homc1_charge_list).sort_values(by=["Timestamp"])

    # plot HOM C1 vs. X/YCOR 04
    print("COR LENGTH: " + str(len(df_correl_homc1_cor["Timestamp"])))
    plotter.plot_correlation(df_correl_homc1_cor,
                             pv_y=pv_list[2],
                             pv_x=pv_list[0],
                             pv_charge=pv_list[-1],
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column=pv_list[0],
                             error_tolerance=0.000015,
                             x_label=label_list[0],
                             y_label=label_list[2],
                             x_units=unit_list[0],
                             y_units=unit_list[2],
                             x_change_decimal_point=3,
                             same_day=True)

    # plot HOM C1 vs. BPM 02 X/Y
    print("BPM LENGTH: " + str(len(df_correl_homc1_cor["Timestamp"])))
    plotter.plot_correlation(df_correl_homc1_bpm,
                             pv_y=pv_list[2],
                             pv_x=pv_list[1],
                             pv_charge=pv_list[-1],
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column=pv_list[1],
                             error_tolerance=0.000015,
                             x_label=label_list[1],
                             y_label=label_list[2],
                             x_units=unit_list[1],
                             y_units=unit_list[2],
                             x_change_decimal_point=0,
                             same_day=True)


def plot_xcor_5_mon():
    """HOM C1 VS. XCOR 04, over a 5-month period"""
    df_xcor = arch_plotter.create_df(arch_plotter.pv("XCOR:GUNB:713:BACT", "2024/01/01 00:00:00",
                                                     "2024/07/02 23:59:59"))
    df_chrg_xcor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_xcor, time_margin_seconds=1.5)
    df_correl_chrg_xcor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_xcor, df_homc1, time_margin_seconds=1.5)
    # Correlation of HOM C1 Signal vs. XCOR:GUNB:713/XCOR 04 Magnet
    plotter.plot_correlation(df_correl_chrg_xcor_homc1,
                             pv_y=pv_hom,
                             pv_x=pv_xcor,
                             pv_charge=pv_charge,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column=pv_xcor,
                             error_tolerance=0.000015,
                             x_label="XCOR 04 Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)


def plot_ycor_5_mon():
    """HOM C1 VS. YCOR 04, over a 5-month period"""
    df_ycor = arch_plotter.create_df(arch_plotter.pv("YCOR:GUNB:713:BACT", "2024/01/01 00:00:00",
                                                     "2024/07/02 23:59:59"))
    df_chrg_ycor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_ycor, time_margin_seconds=1.5)
    df_correl_chrg_ycor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_ycor, df_homc1, time_margin_seconds=1.5)
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:713/YCOR 04 Magnet
    plotter.plot_correlation(df_correl_chrg_ycor_homc1,
                             pv_y=pv_hom,
                             pv_x=pv_ycor,
                             pv_charge=pv_charge,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column=pv_ycor,
                             error_tolerance=0.000015,
                             x_label="YCOR 04 Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)


def plot_bpmx_5_mon():
    """HOM C1 VS. BPM 02 X, over a 5-month period"""
    df_bpmx = arch_plotter.create_df(arch_plotter.pv("BPMS:GUNB:925:X", "2024/01/01 00:00:00",
                                                     "2024/07/02 23:59:59"))
    df_chrg_bpmx = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmx, time_margin_seconds=1.5)
    df_correl_chrg_bpmx_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmx, df_homc1, time_margin_seconds=1.5)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:925:X/BPM 02 X
    plotter.plot_correlation(df_correl_chrg_bpmx_homc1,
                             pv_y=pv_hom,
                             pv_x=pv_bpmx,
                             pv_charge=pv_charge,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column=pv_bpmx,
                             error_tolerance=0.000015,
                             x_label="BPM 02 X",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(mm)",
                             y_units="(arb. units)",
                             x_change_decimal_point=0)


def plot_bpmy_5_mon():
    """HOM C1 VS. BPM 02 Y, over a 5-month period"""
    df_bpmy = arch_plotter.create_df(arch_plotter.pv("BPMS:GUNB:925:Y", "2024/01/01 00:00:00", "2024/07/02 23:59:59"))
    df_chrg_bpmy = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmy, time_margin_seconds=1.5)
    df_correl_chrg_bpmy_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmy, df_homc1, time_margin_seconds=1.5)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:925:Y/BPM 02 Y
    plotter.plot_correlation(df_correl_chrg_bpmy_homc1,
                             pv_y=pv_hom,
                             pv_x=pv_bpmy,
                             pv_charge=pv_charge,
                             charge_val=CHARGE_VAL,
                             charge_tolerance=0.1,
                             plot_error_bars=False,
                             low_vary_column=pv_bpmy,
                             error_tolerance=0.000015,
                             x_label="BPM 02 Y",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(mm)",
                             y_units="(arb. units)",
                             x_change_decimal_point=0)


def plot_xcor_bpmx_phase():
    """HOM C1 VS. XCOR 04, BPM 02 X for XCOR 04/BPM 02 X Buncher Phase Scan"""
    pvs_xcor_bpmx_phase = [pv_xcor, pv_bpmx, pv_hom, pv_charge]
    labels_xcor_bpmx_phase = ["XCOR 04 Magnet", "BPM 02 X", "HOM C1 Signal", "Charge"]
    units_xcor_bpmx_phase = ["(g/m)", "(mm)", "(arbitrary units)"]
    plot_over_time_and_correlation(start_end_dates, pvs_xcor_bpmx_phase, labels_xcor_bpmx_phase, units_xcor_bpmx_phase)


def plot_ycor_bpmy_phase():
    """HOM C1 VS. YCOR 04, BPM 02 Y for XCOR 04/BPM 02 X Buncher Phase Scan"""
    pvs_ycor_bpmy_phase = [pv_ycor, pv_bpmy, pv_hom, pv_charge]
    labels_ycor_bpmy_phase = ["YCOR 04 Magnet", "BPM 02 Y", "HOM C1 Signal", "Charge"]
    units_ycor_bpmy_phase = ["(g/m)", "(mm)", "(arbitrary units)"]
    plot_over_time_and_correlation(start_end_dates, pvs_ycor_bpmy_phase, labels_ycor_bpmy_phase, units_ycor_bpmy_phase)


if __name__ == '__main__':
    plotter = cp.ChargePlotter()
    arch_plotter = ap
    CHARGE_VAL = 50.0  # set this to separate out by charge (pC), all values are: 50, 60, 80, 100, 140, 160, 220
    df_homc1 = arch_plotter.create_df(
        arch_plotter.pv("SCOP:AMRF:RF01:AI_MEAS1", "2024/01/01 00:00:00", "2024/07/02 23:59:59"))
    df_homc1 = filter_hom(df_homc1)
    df_chrg = arch_plotter.create_df(
        arch_plotter.pv("TORO:GUNB:360:CHRG", "2024/01/01 00:00:00", "2024/07/02 23:59:59"))
    df_chrg_filtered = plotter.remove_charges_below_value(df_chrg, pv_charge, min_charge_value=15.0)

    df_charge_homc1 = arch_plotter.merge_dfs_with_margin_by_timestamp_column(df_chrg_filtered, df_homc1,
                                                                             time_margin_seconds=1.5)

    # plot_xcor_5_mon()
    # plot_ycor_5_mon()
    # plot_bpmx_5_mon()
    # plot_bpmy_5_mon()
    # plot_xcor_bpmx_phase()
    # plot_ycor_bpmy_phase()
