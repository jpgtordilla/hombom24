import lcls_tools_plotter as lp


class TestLclsToolsPlotter:

    def __init__(self, lptool):
        self.lptool = lptool
        self.all_pvs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW",
                        "BPMS:HTR:120:FW:X_SLOW",
                        "BPMS:HTR:120:FW:Y_SLOW", "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW",
                        "TORO:GUNB:360:CHRG",
                        "SOLN:GUNB:100:BACT",
                        "QUAD:GUNB:212:1:BACT", "SOLN:GUNB:212:BACT", "QUAD:GUNB:212:2:BACT", "XCOR:GUNB:293:BACT",
                        "YCOR:GUNB:293:BACT",
                        "XCOR:GUNB:388:BACT", "YCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "YCOR:GUNB:513:BACT",
                        "XCOR:GUNB:713:BACT",
                        "YCOR:GUNB:713:BACT", "QUAD:GUNB:823:1:BACT", "SOLN:GUNB:823:BACT", "QUAD:GUNB:823:2:BACT",
                        "XCOR:GUNB:927:BACT",
                        "YCOR:GUNB:927:BACT"]
        self.soln_pvs = ["SOLN:GUNB:100:BACT", "SOLN:GUNB:212:BACT", "SOLN:GUNB:823:BACT"]
        self.quad_pvs = ["QUAD:GUNB:212:1:BACT", "QUAD:GUNB:212:2:BACT", "QUAD:GUNB:823:1:BACT", "QUAD:GUNB:823:2:BACT"]
        self.cor_pvs = ["XCOR:GUNB:293:BACT", "XCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "XCOR:GUNB:713:BACT",
                        "XCOR:GUNB:927:BACT",
                        "YCOR:GUNB:293:BACT", "YCOR:GUNB:388:BACT", "YCOR:GUNB:513:BACT", "YCOR:GUNB:713:BACT",
                        "YCOR:GUNB:927:BACT"]
        self.bpm_pvs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW",
                        "BPMS:HTR:120:FW:X_SLOW",
                        "BPMS:HTR:120:FW:Y_SLOW", "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW"]
        self.start_date = "2024/07/02 14:42:36"
        self.end_date = "2024/07/02 15:42:36"

    # WRITE TESTS FOR EACH METHOD, ONE AT A TIME


if __name__ == "__main__":
    test = TestLclsToolsPlotter(lp.LclsToolsPlotter())
    # TESTS
