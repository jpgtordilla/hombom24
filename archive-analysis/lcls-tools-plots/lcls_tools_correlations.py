import lcls_tools_plotter as lp

"""Using the LCLS tools archiver.py class"""

"""
My class lcls_tools_plotter further simplifies the process of plotting PVs and retrieving data. 
The lines in the main method are used for testing. 
"""

# pv lists
all_pvs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW", "BPMS:HTR:120:FW:X_SLOW",
            "BPMS:HTR:120:FW:Y_SLOW", "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW", "TORO:GUNB:360:CHRG", "SOLN:GUNB:100:BACT", 
            "QUAD:GUNB:212:1:BACT", "SOLN:GUNB:212:BACT", "QUAD:GUNB:212:2:BACT", "XCOR:GUNB:293:BACT", "YCOR:GUNB:293:BACT", 
            "XCOR:GUNB:388:BACT", "YCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "YCOR:GUNB:513:BACT", "XCOR:GUNB:713:BACT", 
            "YCOR:GUNB:713:BACT", "QUAD:GUNB:823:1:BACT", "SOLN:GUNB:823:BACT", "QUAD:GUNB:823:2:BACT", "XCOR:GUNB:927:BACT", 
            "YCOR:GUNB:927:BACT"]
soln_pvs = ["SOLN:GUNB:100:BACT", "SOLN:GUNB:212:BACT", "SOLN:GUNB:823:BACT"]
quad_pvs = ["QUAD:GUNB:212:1:BACT", "QUAD:GUNB:212:2:BACT", "QUAD:GUNB:823:1:BACT", "QUAD:GUNB:823:2:BACT"]
cor_pvs = ["XCOR:GUNB:293:BACT", "XCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "XCOR:GUNB:713:BACT", "XCOR:GUNB:927:BACT", 
           "YCOR:GUNB:293:BACT", "YCOR:GUNB:388:BACT", "YCOR:GUNB:513:BACT", "YCOR:GUNB:713:BACT", "YCOR:GUNB:927:BACT"]
bpm_pvs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW", "BPMS:HTR:120:FW:X_SLOW", 
           "BPMS:HTR:120:FW:Y_SLOW", "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW"]

if __name__ == "__main__": 
    lptool = lp.LclsToolsPlotter()
    # plot all magnet data from July 2nd, from noon until 12:30 PM 
    lptool.megaplot_pvs_over_time(all_pvs, "2024/07/02 12:00:00", "2024/07/02 12:30:00")
    # plot correlation between TORO:GUNB:360:CHRG and the SOLN magnets
    lptool.megaplot_correlation("TORO:GUNB:360:CHRG", soln_pvs, "2024/07/02 12:00:00", "2024/07/02 12:30:00")
    # plot correlation between TORO:GUNB:360:CHRG and the QUAD magnets
    lptool.megaplot_correlation("TORO:GUNB:360:CHRG", quad_pvs, "2024/07/02 12:00:00", "2024/07/02 12:30:00")
    # plot correlation between TORO:GUNB:360:CHRG and the XCOR/YCOR magnets
    lptool.megaplot_correlation("TORO:GUNB:360:CHRG", cor_pvs, "2024/07/02 12:00:00", "2024/07/02 12:30:00")
    # plot correlation between TORO:GUNB:360:CHRG and the BPMs
    lptool.megaplot_correlation("TORO:GUNB:360:CHRG", bpm_pvs, "2024/07/02 12:00:00", "2024/07/02 12:30:00")

# TODO: HOM signal correlations (ideas)
# - process HOM signals
# - method that can plot columns from a df (such as HOM and TORO:...:CHRG)
# - method to convert whatever HOM data timestamps are to the same format as lcls-tools 
# - correlation between HOM signals and TORO:...:CHRG
