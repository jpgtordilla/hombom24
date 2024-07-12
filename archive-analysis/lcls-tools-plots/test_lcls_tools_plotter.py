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
        self.charge_pv = "SOLN:GUNB:360:CHRG"
        self.start_date = "2024/07/02 14:42:36"
        self.end_date = "2024/07/02 15:42:36"

    """PEAK FILTERING TESTS"""

    def test_return_peaks(self):
        df_peak_list = self.lptool.test_return_peaks(pv_list=self.bpm_pvs, start=self.start_date, end=self.end_date,
                                                     peak_height=1, peak_spacing=10)
        print(df_peak_list)  # print the list
        print(df_peak_list[0].head(10))  # see the first 10 entries of the first item
        return

    def test_plot_return_peaks(self):
        # test basic correlation
        df_peak_list = self.lptool.test_return_peaks(pv_list=[self.quad_pvs[0], self.bpm_pvs[0]], start=self.start_date,
                                                     end=self.end_date, peak_height=1, peak_spacing=10, is_correl=True)
        print(df_peak_list)  # print the list
        print(df_peak_list[0].head(10))  # see the first 10 entries of the first item
        # test charge correlation
        return

    def test_return_peaks_from_df(self):
        # TEST BASIC CORRELATION DATAFRAME
        # create DataFrames and merge them together
        df_quad = self.lptool.create_df(pv_str=self.quad_pvs[0], start=self.start_date, end=self.end_date)
        df_cor = self.lptool.create_df(pv_str=self.cor_pvs[0], start=self.start_date, end=self.end_date)
        df_bpms = self.lptool.create_df(pv_str=self.bpm_pvs[0], start=self.start_date, end=self.end_date)
        df_basic_both = self.lptool.create_correlation_df(df_quad, df_cor, self.start_date, self.end_date)
        df_basic_all = self.lptool.create_correlation_df(df_basic_both, df_bpms, self.start_date, self.end_date)
        # run method
        df_peak_list = self.lptool.return_peaks_from_df(df=df_basic_all, peak_height=1.0, peak_spacing=10.0)
        print(df_peak_list)
        print(df_peak_list[0].head(10))

        # TEST CHARGE CORRELATION DATAFRAME
        # TODO: replace with actual charge value
        df_charge_all = self.lptool.create_correlation_charge_df(pv_charge=self.charge_pv, pv_one=self.cor_pvs[0],
                                                                 pv_two=self.bpm_pvs[0], start=self.start_date,
                                                                 end=self.end_date, charge=20.0, tolerance=0.05)
        df_peak_charge_list = self.lptool.return_peaks_from_df(df=df_charge_all, peak_height=1.0, peak_spacing=10.0)
        print(df_peak_charge_list)
        print(df_peak_charge_list[0].head(10))

        # TODO: test with non-archived HOM signal
        return

    def test_plot_peaks_from_df(self):
        # TEST CHARGE CORRELATION DATAFRAME
        # TODO: replace with actual charge value
        df_charge_all = self.lptool.create_correlation_charge_df(pv_charge=self.charge_pv, pv_one=self.cor_pvs[0],
                                                                 pv_two=self.bpm_pvs[0], start=self.start_date,
                                                                 end=self.end_date, charge=20.0, tolerance=0.05)
        df_peak_charge_list = self.lptool.plot_peaks_from_df(df=df_charge_all, peak_height=1.0, peak_spacing=10.0)
        print(df_peak_charge_list)
        print(df_peak_charge_list[0].head(10))
        # TODO: test with non-archived HOM signal
        return

    """CORRELATIONS"""
    def test_plot_correlation(self):
        self.lptool.plot_correlation([self.cor_pvs[0], self.bpm_pvs[0]], start=self.start_date, end=self.end_date)
        self.lptool.plot_correlation([self.cor_pvs[0], self.bpm_pvs[0], self.charge_pv], start=self.start_date,
                                     end=self.end_date, charge=20.0, tolerance=0.05)
        return

    def test_megaplot_correlation_charge_separated(self):
        self.lptool.megaplot_correlation_charge_separated(pv_x=self.cor_pvs[0], pv_y=self.bpm_pvs[0],
                                                          pv_charge=self.charge_pv, start=self.start_date,
                                                          end=self.end_date)
        self.lptool.megaplot_correlation_charge_separated(pv_x=self.quad_pvs[0], pv_y=self.bpm_pvs[0],
                                                          pv_charge=self.charge_pv, start=self.start_date,
                                                          end=self.end_date)
        return


if __name__ == "__main__":
    test = TestLclsToolsPlotter(lp.LclsToolsPlotter())
    # TESTS
    test.test_return_peaks()
    # test.test_plot_return_peaks()
    # test.test_return_peaks_from_df()
    # test.test_plot_peaks_from_df()
    # test.test_plot_correlation()
    # test.test_megaplot_correlation_charge_separated()


