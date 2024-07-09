import lcls_tools_plotter as lp

"""Using the LCLS tools archiver.py class"""

"""
My class lcls_tools_plotter further simplifies the process of plotting PVs and retrieving data. 
"""

def main():
    lptool = lp.LclsToolsPlotter()
    # create df
    df = lptool.create_df(pv_str="SOLN:GUNB:100:BACT", start="2024/07/02 14:42:36", end="2024/07/02 15:42:36") # useful if you want to simply create a df of a single pv 
    print(df.head)
    # plot over time
    lptool.plot_pv_over_time(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")

if __name__ == "__main__": 
    main()