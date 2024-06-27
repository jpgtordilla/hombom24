import archviewer as av

# USING THE ARCHVIEWER TOOL EXAMPLE

avtool = av.ArchViewer()

# must first convert to df, use the absolute path name for a csv file
df = avtool.csv_to_df("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/archviewer-plots/test-vis/1m-soln-gunb-100.csv") # provide absolute path

# plots are shown one at a time
avtool.specific_col_plot(df, "SOLN:GUNB:100:BMON", "kG")
avtool.megaplot_all_cols(df, "kG")
avtool.spec_correl(df, df, "SOLN:GUNB:100:BMON", "SOLN:GUNB:100:IMON")