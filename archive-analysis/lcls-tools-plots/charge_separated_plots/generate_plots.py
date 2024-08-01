import charge_separator as cs
import charge_plotter as cp
import pandas as pd

if __name__ == '__main__':
    plotter = cp.ChargePlotter()

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

    # SECTION 2: HOM C1 VS. YCOR AND BPMS:Y, 6 MONTH PERIOD

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


