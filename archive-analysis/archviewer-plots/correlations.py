import archviewer as av

"""PLOTTING CORRELATIONS: use this script to compare with MEME and lcls-tools archiver.py"""

def main(): 
    avtool = av.ArchViewer()
    df = avtool.csv_to_df("/Users/jonathontordilla/Desktop/hombom24/archive-analysis/archviewer-plots/hom-data/feb_hom_with_charge.csv")
    avtool.correl(df, "BPMS:L0B:0183:FW:X_SLOW", df, start=0, end=10000)
    avtool.megaplot_all_cols(df, "mm", start=0, end=10000)
    print(df.columns) # use this object to determine what correlations can be generated
    
    # TODO: generate correlations to determine charge relationship

if __name__ == "__main__": 
    main()