import archiver_plotter as ap
archplot = ap.ArchiverPlotter()

# Create variables to represent PVs and datetimes
xcor_pv = "XCOR:GUNB:293:BACT"
ycor_pv = "YCOR:GUNB:293:BACT"
homc1_pv = "SCOP:AMRF:RF01:AI_MEAS1"
start_str = "2024/07/02 12:00:00"
end_str = "2024/07/02 13:00:00"

# Create DataFrames for PVs
df_xcor = archplot.create_df(xcor_pv, start_str, end_str)
df_ycor = archplot.create_df(ycor_pv, start_str, end_str)
df_homc1 = archplot.create_df(homc1_pv, start_str, end_str)

# Create a DataFrame for the correlation between two PVs
df_correl = archplot.create_correlation_df(df_xcor, df_homc1)

# Plot a list of PVs over time
archplot.plot_pv_over_time([df_xcor, df_ycor], pv_labels=["XCOR", "YCOR"], ylabel_left="mm")

# Plot a correlation between two PVs using their correlation DataFrame and String identifiers
archplot.plot_correlation(df_correl, xcor_pv, homc1_pv, pv_xlabel="XCOR (mm)", pv_ylabel="HOM C1 (arb. units)",
                          smart_labels=True)
