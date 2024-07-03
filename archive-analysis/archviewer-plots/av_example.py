import archviewer as av

"""USING THE ARCHVIEWER TOOL EXAMPLE"""

"""
To view data, you must first download a csv. 
This csv can have any start or end time, as long as the desired interval is contained within. 
When plotting data over a timeframe, please specify the start and end time in number of seconds. 
"""

def main():
    avtool = av.ArchViewer()
    # must first convert to df, use the absolute path name for a csv file
    df = avtool.csv_to_df("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/archviewer-plots/test-vis/1m-soln-gunb-100.csv") # provide absolute path
    bpm = avtool.csv_to_df("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/archviewer-plots/test-vis/2w-bpms-gunb-314-x.csv")
    # create plots
    avtool.specific_col_plot(df, "SOLN:GUNB:100:BMON", "kG", start=0, end=35)
    avtool.megaplot_all_cols(df, "kG", start=0, end=35)
    avtool.spec_correl(df, df, "SOLN:GUNB:100:BMON", "SOLN:GUNB:100:IMON", start=0, end=35)
    avtool.plot_return_peaks(bpm, "Timestamp", "BPMS:GUNB:314:X", "mm", peak_height=1, peak_dist=10, x_start=0, x_end=1000)
    print(avtool.return_peaks(bpm, "BPMS:GUNB:314:X", peak_height=1, peak_dist=10, x_start=0, x_end=1000))

if __name__ == "__main__": 
    main()