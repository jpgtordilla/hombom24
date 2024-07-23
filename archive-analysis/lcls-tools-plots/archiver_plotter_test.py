import archiver_plotter as ap

# VARIABLES
aptest = ap.ArchiverPlotter()
chrg_pv = "TORO:GUNB:360:CHRG"
homc1_pv = "SCOP:AMRF:RF01:AI_MEAS1"
start_str = "2024/07/02 12:00:00"
end_str = "2024/07/02 13:00:00"

# TESTS: creating DataFrames
df_chrg = aptest.create_df(chrg_pv, start_str, end_str)
df_homc1 = aptest.create_df(homc1_pv, start_str, end_str)
df_correl = aptest.create_correlation_df(df_chrg, df_homc1)

# TESTS: plotting
aptest.plot_pv_over_time([df_chrg, df_homc1], start_str, end_str)
aptest.plot_correlation(df_correl, chrg_pv, homc1_pv, start_str, end_str)