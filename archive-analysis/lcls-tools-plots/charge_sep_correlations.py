import lcls_tools_plotter as lp

"""Using the LCLS tools archiver.py class"""

"""
My class lcls_tools_plotter further simplifies the process of plotting PVs and retrieving data. 
The lines in the main method are used for testing. 
"""

pv_names = ['BPMS:L0B:0183:FW:X_SLOW',
            'BPMS:L0B:0183:FW:Y_SLOW',
            'BPMS:HTR:120:FW:X_SLOW',
            'BPMS:HTR:120:FW:Y_SLOW',
            'BPMS:GUNB:925:FW:X_SLOW',
            'BPMS:GUNB:925:FW:Y_SLOW',
            'SCOP:AMRF:RF01:AI_MEAS1',
            'SCOP:AMRF:RF01:AI_MEAS2',
            'SCOP:AMRF:RF01:AI_MEAS3',
            'SCOP:AMRF:RF01:AI_MEAS4',
            'SCOP:AMRF:RF03:AI_MEAS1',
            'SCOP:AMRF:RF03:AI_MEAS2',
            'SCOP:AMRF:RF03:AI_MEAS3',
            'SCOP:AMRF:RF03:AI_MEAS4',
            'TORO:GUNB:360:CHRG']

plot_names = ['CM BPM X',
              'CM BPM Y',
              'HTR BPM X',
              'HTR BPM Y',
              'GUN BPM X',
              'GUN BPM Y',
              'HOM C1',
              'HOM C2',
              'HOM C3',
              'HOM C4',
              'HOM C5',
              'HOM C6',
              'HOM C7',
              'HOM C8',
              'Charge']

timestamps = {"start": "2024/05/01 11:00:00",
              "end": "2024/05/01 13:00:00"}


def examples():
    """EXAMPLES"""
    # Generate mean charge values within the given timeframe
    charge_vals = lptool.get_common_charges(pv_charge="TORO:GUNB:360:CHRG", cutoff=0.1, tolerance=0.1,
                                            start=timestamps["start"], end=timestamps["end"])
    print(charge_vals)
    # HOM C1 vs. charge
    lptool.plot_correlation(pv_list=["TORO:GUNB:360:CHRG", "SCOP:AMRF:RF01:AI_MEAS1"],
                            start=timestamps["start"], end=timestamps["end"], charge=charge_vals[10],
                            tolerance=0.05)
    # HOM C1 vs. CM BPM X for a given charge
    lptool.plot_correlation(pv_list=['BPMS:L0B:0183:FW:X_SLOW', 'SCOP:AMRF:RF01:AI_MEAS1', 'TORO:GUNB:360:CHRG'],
                            start=timestamps["start"], end=timestamps["end"], charge=charge_vals[10],
                            tolerance=0.05)
    # HOM C1 vs. CM BPM X for all charges
    lptool.megaplot_correlation_charge_separated(pv_x='BPMS:L0B:0183:FW:X_SLOW', pv_y='SCOP:AMRF:RF01:AI_MEAS1',
                                                 pv_charge='TORO:GUNB:360:CHRG', start=timestamps["start"],
                                                 end=timestamps["end"], charge_vals=charge_vals)


def ipac_plots():
    """SIMILAR TO IPAC24 PLOTS"""
    # HOM C1 Signal vs. Charge (signal increases with charge)
    lptool.plot_correlation(pv_list=["TORO:GUNB:360:CHRG", "SCOP:AMRF:RF01:AI_MEAS1"], start=timestamps["start"],
                            end=timestamps["end"])
    # HOM C5 Signal vs. Charge (more misalignment at C1, entering at an angle)
    lptool.plot_correlation(pv_list=["TORO:GUNB:360:CHRG", "SCOP:AMRF:RF03:AI_MEAS1"], start=timestamps["start"],
                            end=timestamps["end"])

    # HOM 1 and HOM 5 over time
    lptool.plot_pv_over_time(pv_list=["SCOP:AMRF:RF01:AI_MEAS1", "SCOP:AMRF:RF03:AI_MEAS1"],
                             start=timestamps["start"], end=timestamps["end"])

    # All HOM signals over time
    lptool.plot_pv_over_time(pv_list=pv_names[6:-1], start=timestamps["start"],
                             end=timestamps["end"])

    # GUN BPM X and GUN BPM Y over time
    lptool.plot_pv_over_time(pv_list=pv_names[4:6], start=timestamps["start"], end=timestamps["end"])


if __name__ == "__main__":
    lptool = lp.LclsToolsPlotter()
    examples()
    ipac_plots()
