import lcls_tools_plotter as lp

class TestLclsToolsPlotter(): 

    def __init__(self, lptool): 
        self.lptool = lptool

    def test_plot(self): 
        # plot one pv over time
        self.lptool.plot_pv_over_time(pv_list=["SOLN:GUNB:100:BACT"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        # plot 2 pvs over time
        self.lptool.plot_pv_over_time(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        # plot 3 pvs over time
        self.lptool.plot_pv_over_time(pv_list=["YCOR:GUNB:293:BACT", "XCOR:GUNB:388:BACT", "YCOR:GUNB:388:BACT"], start="2024/07/02 14:42:36", end="2024/07/02 14:42:56")

    def test_mega(self): 
        # megaplot of 1 pv over time
        self.lptool.megaplot_pvs_over_time(pv_list=["BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        # megaplot of 2 pvs over time
        self.lptool.megaplot_pvs_over_time(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        # megaplot of 3 pvs over time
        self.lptool.megaplot_pvs_over_time(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW", "YCOR:GUNB:293:BACT"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        # megaplot of 4 pvs over time
        self.lptool.megaplot_pvs_over_time(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW", "YCOR:GUNB:293:BACT", "XCOR:GUNB:927:BACT"], start="2024/07/02 14:42:36", end="2024/07/02 14:52:36")
        # megaplot of all pvs over time
        all_pvs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW", "BPMS:HTR:120:FW:X_SLOW", "BPMS:HTR:120:FW:Y_SLOW", 
                   "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW", "TORO:GUNB:360:CHRG", "SOLN:GUNB:100:BACT", "QUAD:GUNB:212:1:BACT", "SOLN:GUNB:212:BACT",
                   "QUAD:GUNB:212:2:BACT", "XCOR:GUNB:293:BACT", "YCOR:GUNB:293:BACT", "XCOR:GUNB:388:BACT", "YCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "YCOR:GUNB:513:BACT",
                   "XCOR:GUNB:713:BACT", "YCOR:GUNB:713:BACT", "QUAD:GUNB:823:1:BACT", "SOLN:GUNB:823:BACT", "QUAD:GUNB:823:2:BACT", "XCOR:GUNB:927:BACT", "YCOR:GUNB:927:BACT"]
        self.lptool.megaplot_pvs_over_time(pv_list=all_pvs, start="2024/07/02 14:42:36", end="2024/07/02 14:43:36")

    def test_peaks(self): 
        # dictionary of peaks for 1 pv
        print(self.lptool.return_peaks(pv_list=["BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36", peak_height=0.2, peak_spacing=10))
        # dictionary of peaks for 2 pvs
        print(self.lptool.return_peaks(pv_list=["BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36", peak_height=0.2, peak_spacing=10))
        # dictionary of peaks and plot for 1 pv
        print(self.lptool.plot_return_peaks(pv_list=["BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36", peak_height=0.2, peak_spacing=10))
        # dictionary of peaks and plot for 2 pvs
        print(self.lptool.plot_return_peaks(pv_list=["BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36", peak_height=0.2, peak_spacing=10))

    def test_correlation(self): 
        self.lptool.plot_correlation("SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW", start="2024/07/02 14:42:36", end="2024/07/02 15:42:36")
        self.lptool.plot_return_peaks(pv_list=["SOLN:GUNB:100:BACT", "BPMS:L0B:0183:FW:X_SLOW"], start="2024/07/02 14:42:36", end="2024/07/02 15:42:36", peak_height=0.2, peak_spacing=1, is_correl=True)

if __name__ == "__main__": 
    test = TestLclsToolsPlotter(lp.LclsToolsPlotter())
    # TESTS
    # test.test_plot()
    # test.test_mega()
    # test.test_peaks()
    # test.test_correlation()