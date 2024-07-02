import archviewer as av

"""USING THE ARCHVIEWER TOOL EXAMPLE"""

avtool = av.ArchViewer()

# must first convert to df, use the absolute path name for a csv file
df = avtool.csv_to_df("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/archviewer-plots/hom-data/feb_hom_with_charge.csv")

avtool.correl(df, "BPMS:L0B:0183:FW:X_SLOW", df, start=0, end=10000)
avtool.megaplot_all_cols(df, "mm", start=0, end=10000)
print(df)