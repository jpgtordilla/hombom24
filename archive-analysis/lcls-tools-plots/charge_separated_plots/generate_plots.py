import charge_separator as cs
import charge_plotter as cp
import pandas as pd
import sys
sys.path.append("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/archiver_plotter")
import archiver_plotter as ap  # type: ignore


def section_1():
    # Correlation of HOM C1 Signal vs. XCOR 293 Magnet (no error bars)
    plotter.plot_correlation(df_correl_chrg_xcor_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="XCOR:GUNB:293:BACT",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column="XCOR:GUNB:293:BACT",
                             error_tolerance=0.000015,
                             x_label="XCOR Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)
    # Correlation of HOM C1 Signal vs. XCOR:GUNB:293 Magnet (with error bars)
    plotter.plot_correlation(df_correl_chrg_xcor_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="XCOR:GUNB:293:BACT",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=True,
                             low_vary_column="XCOR:GUNB:293:BACT",
                             error_tolerance=0.000015,
                             x_label="XCOR Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)
    # Correlation of HOM C1 Signal vs. XCOR:GUNB:513 (with error bars)
    # Correlation of HOM C1 Signal vs. XCOR:GUNB:713 (with error bars)
    # Correlation of HOM C1 Signal vs. XCOR:GUNB:927 (with error bars)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:314:X (no error bars)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:925:X (no error bars)
    plotter.plot_correlation(df_correl_chrg_bpmx_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="BPMS:GUNB:925:X",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column="BPMS:GUNB:925:X",
                             error_tolerance=0.000015,
                             x_label="BPM X",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(mm)",
                             y_units="(arb. units)",
                             x_change_decimal_point=0)


def section_2():
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:293 Magnet (no error bars)
    plotter.plot_correlation(df_correl_chrg_ycor_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="YCOR:GUNB:293:BACT",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column="YCOR:GUNB:293:BACT",
                             error_tolerance=0.000015,
                             x_label="YCOR Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:293 Magnet (with error bars)
    plotter.plot_correlation(df_correl_chrg_ycor_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="YCOR:GUNB:293:BACT",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=True,
                             low_vary_column="YCOR:GUNB:293:BACT",
                             error_tolerance=0.000015,
                             x_label="YCOR Magnet",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(g/m)",
                             y_units="(arb. units)",
                             x_change_decimal_point=3)
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:513 (with error bars)
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:713 (with error bars)
    # Correlation of HOM C1 Signal vs. YCOR:GUNB:927 (with error bars)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:314:Y (no error bars)
    # Correlation of HOM C1 Signal vs. BPMS:GUNB:925:Y (no error bars)
    plotter.plot_correlation(df_correl_chrg_bpmy_homc1,
                             pv_y="SCOP:AMRF:RF01:AI_MEAS1",
                             pv_x="BPMS:GUNB:925:Y",
                             pv_charge="TORO:GUNB:360:CHRG",
                             charge_val=50.0, charge_tolerance=0.5,
                             plot_error_bars=False,
                             low_vary_column="BPMS:GUNB:925:Y",
                             error_tolerance=0.000015,
                             x_label="BPM Y",
                             y_label="HOM C1 Signal",
                             y_vary=True,
                             x_num_rounded_digits=5,
                             y_num_rounded_digits=2,
                             x_units="(mm)",
                             y_units="(arb. units)",
                             x_change_decimal_point=0)
    # Correlation of HOM C1 Signal vs. BPMS:L0B:0183:Y (no error bars)
    # Correlation of HOM C1 Signal vs. BPMS:HTR:120:Y (no error bars)


def plot_over_time_and_correlation(date_list, pv_list, label_list, unit_list):
    # pv_list = ["YCOR:GUNB:293:BACT", "BPMS:GUNB:925:Y", "SCOP:AMRF:RF01:AI_MEAS1", "TORO:GUNB:360:CHRG"]
    # label_list = ["YCOR Magnet", "BPM Y", "HOM C1 Signal", "Charge"]
    # unit_list = ["g/m", "mm", "arbitrary units"]

    # PLOT OVER TIME FOR A SHORT TIMEFRAME
    range_start_date = date_list[0][0]
    range_end_date = date_list[0][1]
    # create DataFrames for the PV over time
    df_cor = arch_plotter.create_df(pv_list[0], range_start_date, range_end_date)
    df_bpm = arch_plotter.create_df(pv_list[1], range_start_date, range_end_date)
    df_hom = arch_plotter.create_df(pv_list[2], range_start_date, range_end_date)
    # plot over time
    # arch_plotter.plot_pv_over_time([df_cor, df_bpm, df_hom], is_scatter=True)
    arch_plotter.plot_pv_over_time([df_cor, df_bpm], is_scatter=True)
    arch_plotter.plot_pv_over_time([df_cor, df_hom], is_scatter=True)
    arch_plotter.plot_pv_over_time([df_bpm, df_hom], is_scatter=True)
    # arch_plotter.plot_pv_over_time([df_cor])
    # arch_plotter.plot_pv_over_time([df_bpm])
    # arch_plotter.plot_pv_over_time([df_hom])

    # COMBINE TIMEFRAMES AND FIND CORRELATIONS

    correl_homc1_cor_list = []
    correl_homc1_bpm_list = []
    for x in range(5):
        curr_start_date = date_list[x][0]
        curr_end_date = date_list[x][1]

        # create DataFrames
        df_cor = arch_plotter.create_df(pv_list[0], curr_start_date, curr_end_date)
        df_bpm = arch_plotter.create_df(pv_list[1], curr_start_date, curr_end_date)
        df_hom = arch_plotter.create_df(pv_list[2], curr_start_date, curr_end_date)
        df_charge = arch_plotter.create_df(pv_list[3], curr_start_date, curr_end_date)

        # create correlations and add to list
        df_charge_filtered = plotter.remove_charges_below_value(df_charge, pv_list[-1], 15.0)
        df_charge_cor = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_cor, time_margin_seconds=10)
        df_charge_bpm = plotter.merge_with_margin_on_timestamp(df_charge_filtered, df_bpm, time_margin_seconds=10)
        df_correl_homc1_cor = plotter.merge_with_margin_on_timestamp(df_charge_cor, df_hom, time_margin_seconds=10)
        df_correl_homc1_bpm = plotter.merge_with_margin_on_timestamp(df_charge_bpm, df_hom, time_margin_seconds=10)

        correl_homc1_cor_list.append(df_correl_homc1_cor)
        correl_homc1_bpm_list.append(df_correl_homc1_bpm)

    # combine dataframes from list and sort
    df_correl_homc1_cor = pd.concat(correl_homc1_cor_list).sort_values(by=["Timestamp"])
    df_correl_homc1_bpm = pd.concat(correl_homc1_bpm_list).sort_values(by=["Timestamp"])

    # plot HOM C1 vs. COR
    plotter.plot_correlation(df_correl_homc1_cor,
                             pv_y=pv_list[2],
                             pv_x=pv_list[0],
                             pv_charge=pv_list[-1],
                             charge_val=50.0,
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
    plotter.plot_correlation(df_correl_homc1_cor,
                             pv_y=pv_list[2],
                             pv_x=pv_list[0],
                             pv_charge=pv_list[-1],
                             charge_val=50.0,
                             charge_tolerance=0.5,
                             plot_error_bars=True,
                             low_vary_column=pv_list[0],
                             error_tolerance=0.000015,
                             x_label=label_list[0],
                             y_label=label_list[2],
                             x_units=unit_list[0],
                             y_units=unit_list[2],
                             x_change_decimal_point=3,
                             same_day=True)

    # plot HOM C1 vs. BPM
    plotter.plot_correlation(df_correl_homc1_bpm,
                             pv_y=pv_list[2],
                             pv_x=pv_list[1],
                             pv_charge=pv_list[-1],
                             charge_val=50.0,
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


if __name__ == '__main__':
    plotter = cp.ChargePlotter()
    arch_plotter = ap.ArchiverPlotter()

    # CREATE DATAFRAMES FROM ARCHIVE DATA
    df_homc1 = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data"
        "/SCOP_AMRF_RF01_AI_MEAS1_6M.csv")
    df_chrg = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data"
        "/TORO_GUNB_360_CHRG_6M.csv")
    df_xcor = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data/"
        "XCOR_GUNB_293_BACT_6M.csv")
    df_ycor = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data"
        "/YCOR_GUNB_293_BACT_6M.csv")
    df_bpmx = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data/"
        "BPMS_GUNB_925_X_6M.csv"
    )
    df_bpmy = pd.read_csv(
        "/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/charge_separated_plots/epics_data/"
        "BPMS_GUNB_925_Y_6M.csv"
    )

    # CREATE A DATAFRAME WITH COLUMNS FOR EACH PV, ALIGNED BY TIMEFRAME
    df_chrg_filtered = plotter.remove_charges_below_value(df_chrg, "TORO:GUNB:360:CHRG", min_charge_value=15.0)
    df_chrg_ycor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_ycor, time_margin_seconds=1.5)
    df_chrg_xcor = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_xcor, time_margin_seconds=1.5)
    df_chrg_bpmx = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmx, time_margin_seconds=1.5)
    df_chrg_bpmy = plotter.merge_with_margin_on_timestamp(df_chrg_filtered, df_bpmy, time_margin_seconds=1.5)
    df_correl_chrg_ycor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_ycor, df_homc1, time_margin_seconds=1.5)
    df_correl_chrg_xcor_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_xcor, df_homc1, time_margin_seconds=1.5)
    df_correl_chrg_bpmx_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmx, df_homc1, time_margin_seconds=1.5)
    df_correl_chrg_bpmy_homc1 = plotter.merge_with_margin_on_timestamp(df_chrg_bpmy, df_homc1, time_margin_seconds=1.5)

    # check if there are enough data points in the plot: prints True if there is
    print(len(df_correl_chrg_ycor_homc1["Timestamp"]) >= 50)
    print(len(df_correl_chrg_xcor_homc1["Timestamp"]) >= 50)
    print(len(df_correl_chrg_bpmy_homc1["Timestamp"]) >= 50)
    print(len(df_correl_chrg_bpmx_homc1["Timestamp"]) >= 50)

    # SECTION 1: HOM C1 VS. XCOR AND BPMS:X, 6 MONTH PERIOD

    # section_1()

    # SECTION 2: HOM C1 VS. YCOR AND BPMS:Y, 6 MONTH PERIOD

    # section_2()

    # SECTION 3: HOM C1 VS. XCOR, BPM X FOR HIGH XCOR ACTIVITY

    start_end_dates_sec_3 = [("2024/07/02 00:00:00", "2024/07/02 00:30:00"),
                             ("2024/07/02 02:00:00", "2024/07/02 02:30:00"),
                             ("2024/07/02 12:00:00", "2024/07/02 12:30:00"),
                             ("2024/07/02 03:00:16", "2024/07/02 03:28:41"),
                             ("2024/07/02 01:30:04", "2024/07/02 01:55:51")]
    pvs_sec_3 = ["XCOR:GUNB:293:BACT", "BPMS:GUNB:925:X", "SCOP:AMRF:RF01:AI_MEAS1", "TORO:GUNB:360:CHRG"]
    label_list_sec_3 = ["XCOR Magnet", "BPM X", "HOM C1 Signal", "Charge"]
    unit_list_sec_3 = ["(g/m)", "(mm)", "(arbitrary units)"]

    plot_over_time_and_correlation(start_end_dates_sec_3, pvs_sec_3, label_list_sec_3, unit_list_sec_3)

    # SECTION 4: HOM C1 VS. YCOR, BPM Y FOR HIGH XCOR ACTIVITY

    start_end_dates_sec_4 = [("2024/07/02 00:00:00", "2024/07/02 00:30:00"),
                             ("2024/07/02 02:00:00", "2024/07/02 02:30:00"),
                             ("2024/07/02 12:00:00", "2024/07/02 12:30:00"),
                             ("2024/07/02 03:00:16", "2024/07/02 03:28:41"),
                             ("2024/07/02 01:30:04", "2024/07/02 01:55:51")]
    pvs_sec_4 = ["YCOR:GUNB:293:BACT", "BPMS:GUNB:925:Y", "SCOP:AMRF:RF01:AI_MEAS1", "TORO:GUNB:360:CHRG"]
    label_list_sec_4 = ["YCOR Magnet", "BPM Y", "HOM C1 Signal", "Charge"]
    unit_list_sec_4 = ["(g/m)", "(mm)", "(arbitrary units)"]

    plot_over_time_and_correlation(start_end_dates_sec_4, pvs_sec_4, label_list_sec_4, unit_list_sec_4)

