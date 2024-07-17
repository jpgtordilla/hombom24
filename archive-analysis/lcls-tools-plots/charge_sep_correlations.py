import lcls_tools_plotter as lp

"""Using the LCLS tools archiver.py class"""

"""
My class lcls_tools_plotter further simplifies the process of plotting PVs and retrieving data. 
The lines in the main method are used for testing. 
"""

HOM_PVs = ['SCOP:AMRF:RF01:AI_MEAS1',
           'SCOP:AMRF:RF01:AI_MEAS2',
           'SCOP:AMRF:RF01:AI_MEAS3',
           'SCOP:AMRF:RF01:AI_MEAS4',
           'SCOP:AMRF:RF03:AI_MEAS1',
           'SCOP:AMRF:RF03:AI_MEAS2',
           'SCOP:AMRF:RF03:AI_MEAS3',
           'SCOP:AMRF:RF03:AI_MEAS4']

SOLN_PVs = ["SOLN:GUNB:100:BACT", "SOLN:GUNB:212:BACT", "SOLN:GUNB:823:BACT"]
QUAD_PVs = ["QUAD:GUNB:212:1:BACT", "QUAD:GUNB:212:2:BACT", "QUAD:GUNB:823:1:BACT", "QUAD:GUNB:823:2:BACT"]
COR_PVs = ["XCOR:GUNB:293:BACT", "XCOR:GUNB:388:BACT", "XCOR:GUNB:513:BACT", "XCOR:GUNB:713:BACT", "XCOR:GUNB:927:BACT",
           "YCOR:GUNB:293:BACT", "YCOR:GUNB:388:BACT", "YCOR:GUNB:513:BACT", "YCOR:GUNB:713:BACT", "YCOR:GUNB:927:BACT"]
BPM_PVs = ["BPMS:GUNB:925:X", "BPMS:GUNB:925:Y", "BPMS:L0B:0183:FW:X_SLOW", "BPMS:L0B:0183:FW:Y_SLOW",
           "BPMS:HTR:120:FW:X_SLOW", "BPMS:HTR:120:FW:Y_SLOW", "BPMS:GUNB:925:FW:X_SLOW", "BPMS:GUNB:925:FW:Y_SLOW"]

HOM_C1_PV = "SCOP:AMRF:RF01:AI_MEAS1"
HOM_C5_PV = "SCOP:AMRF:RF03:AI_MEAS1"
CHARGE_PV = "TORO:GUNB:360:CHRG"

timestamps = {"start": "2024/02/24 16:00:00",
              "end": "2024/02/24 20:00:00"}


def examples():
    """EXAMPLES"""
    # Generate mean charge values within the given timeframe
    charge_vals = lptool.get_common_charges(pv_charge=CHARGE_PV, cutoff=0.1, tolerance=0.2, start=timestamps["start"],
                                            end=timestamps["end"])
    print(f"charge values (pC): {charge_vals}")
    # HOM C1 vs. charge
    lptool.plot_correlation(pv_list=[CHARGE_PV, HOM_C1_PV], start=timestamps["start"], end=timestamps["end"],
                            charge=charge_vals[7], tolerance=0.05)
    # HOM C1 vs. CM BPM X for a given charge
    lptool.plot_correlation(pv_list=['BPMS:L0B:0183:FW:X_SLOW', HOM_C1_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[7], tolerance=0.2)
    # HOM C1 vs. CM BPM X for all charges
    lptool.megaplot_correlation_charge_separated(pv_x='BPMS:L0B:0183:FW:X_SLOW', pv_y=HOM_C1_PV, pv_charge=CHARGE_PV,
                                                 start=timestamps["start"], end=timestamps["end"],
                                                 charge_vals=charge_vals)


def ipac_plots():
    """SIMILAR TO IPAC24 PLOTS"""
    # HOM C1 Signal vs. Charge (signal increases with charge)
    lptool.plot_correlation(pv_list=[CHARGE_PV, HOM_C1_PV], start=timestamps["start"], end=timestamps["end"])
    # HOM C5 Signal vs. Charge (more misalignment at C1, entering at an angle)
    lptool.plot_correlation(pv_list=[CHARGE_PV, HOM_C5_PV], start=timestamps["start"], end=timestamps["end"])
    # HOM 1 and HOM 5 over time
    lptool.plot_pv_over_time(pv_list=[HOM_C1_PV, HOM_C5_PV], start=timestamps["start"], end=timestamps["end"])
    # All HOM signals over time
    lptool.plot_pv_over_time(pv_list=HOM_PVs, start=timestamps["start"], end=timestamps["end"])
    # GUN BPM X and GUN BPM Y over time
    lptool.plot_pv_over_time(pv_list=HOM_PVs, start=timestamps["start"], end=timestamps["end"])


def hom_analysis_xcor():
    # Generate mean charge values within the given timeframe
    charge_vals = lptool.get_common_charges(pv_charge=CHARGE_PV, cutoff=0.1, tolerance=0.2, start=timestamps["start"],
                                            end=timestamps["end"])
    print(f"charge values (pC): {charge_vals}")

    # HOM C1 SIGNAL
    # HOM C1 vs. XCOR:GUNB:293:BACT for all charges
    lptool.megaplot_correlation_charge_separated(pv_x="XCOR:GUNB:293:BACT", pv_y=HOM_C1_PV, pv_charge=CHARGE_PV,
                                                 start=timestamps["start"], end=timestamps["end"],
                                                 charge_vals=charge_vals)
    # HOM C1 vs. XCOR:GUNB:293:BACT for 48.65 pC and 158.17 pC
    lptool.plot_correlation(pv_list=["XCOR:GUNB:293:BACT", HOM_C1_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[7], tolerance=0.2)
    lptool.plot_correlation(pv_list=["XCOR:GUNB:293:BACT", HOM_C1_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[9], tolerance=0.2)

    # HOM C5 SIGNAL
    # HOM C5 vs. XCOR:GUNB:293:BACT for all charges
    lptool.megaplot_correlation_charge_separated(pv_x="XCOR:GUNB:293:BACT", pv_y=HOM_C5_PV, pv_charge=CHARGE_PV,
                                                 start=timestamps["start"], end=timestamps["end"],
                                                 charge_vals=charge_vals)
    # HOM C5 vs. XCOR:GUNB:293:BACT for 48.65 pC and 158.17 pC
    lptool.plot_correlation(pv_list=["XCOR:GUNB:293:BACT", HOM_C5_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[7], tolerance=0.2)
    lptool.plot_correlation(pv_list=["XCOR:GUNB:293:BACT", HOM_C5_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[9], tolerance=0.2)


def hom_analysis_bpmx():
    # Generate mean charge values within the given timeframe
    charge_vals = lptool.get_common_charges(pv_charge=CHARGE_PV, cutoff=0.1, tolerance=0.2, start=timestamps["start"],
                                            end=timestamps["end"])
    print(f"charge values (pC): {charge_vals}")

    # HOM C1 SIGNAL
    # HOM C1 vs. BPMS:GUNB:925:X for all charges
    lptool.megaplot_correlation_charge_separated(pv_x="BPMS:GUNB:925:X", pv_y=HOM_C1_PV, pv_charge=CHARGE_PV,
                                                 start=timestamps["start"], end=timestamps["end"],
                                                 charge_vals=charge_vals)
    # HOM C1 vs. BPMS:GUNB:925:X for 48.65 pC and 158.17 pC
    lptool.plot_correlation(pv_list=["BPMS:GUNB:925:X", HOM_C1_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[7], tolerance=0.2)
    lptool.plot_correlation(pv_list=["BPMS:GUNB:925:X", HOM_C1_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[9], tolerance=0.2)

    # HOM C5 SIGNAL
    # HOM C5 vs. BPMS:GUNB:925:X for all charges
    lptool.megaplot_correlation_charge_separated(pv_x="BPMS:GUNB:925:X", pv_y=HOM_C5_PV, pv_charge=CHARGE_PV,
                                                 start=timestamps["start"], end=timestamps["end"],
                                                 charge_vals=charge_vals)
    # HOM C5 vs. XCOR:GUNB:293:BACT for 48.65 pC and 158.17 pC
    lptool.plot_correlation(pv_list=["BPMS:GUNB:925:X", HOM_C5_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[7], tolerance=0.2)
    lptool.plot_correlation(pv_list=["BPMS:GUNB:925:X", HOM_C5_PV, CHARGE_PV], start=timestamps["start"],
                            end=timestamps["end"], charge=charge_vals[9], tolerance=0.2)


if __name__ == "__main__":
    lptool = lp.LclsToolsPlotter()
    # examples()
    # ipac_plots()
    # hom_analysis_xcor()
    hom_analysis_bpmx()
