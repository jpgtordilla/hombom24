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

timestamps = {"start": "2024/07/02 12:00:00", "end": "2024/07/02 15:00:00"}

if __name__ == "__main__":
    lptool = lp.LclsToolsPlotter()
    # Generate mean charge values within the given timeframe
    charge_vals = lptool.get_common_charges(pv_charge="TORO:GUNB:360:CHRG", cutoff=0.1, tolerance=0.5,
                                            start=timestamps["start"], end=timestamps["end"])
    # Print charge values
    print(charge_vals)
    # HOM C1 vs. charge
    lptool.plot_correlation(pv_list=['TORO:GUNB:360:CHRG', 'SCOP:AMRF:RF01:AI_MEAS1'],
                            start=timestamps['start'], end=timestamps['end'], charge=charge_vals[5], tolerance=0.05)
    # HOM C1 vs. CM BPM X for 67 pC
    lptool.plot_correlation(pv_list=['BPMS:L0B:0183:FW:X_SLOW', 'SCOP:AMRF:RF01:AI_MEAS1', 'TORO:GUNB:360:CHRG'],
                            start=timestamps['start'], end=timestamps['end'], charge=charge_vals[5], tolerance=0.05)
    lptool.megaplot_correlation_charge_separated(pv_x='BPMS:L0B:0183:FW:X_SLOW', pv_y='SCOP:AMRF:RF01:AI_MEAS1',
                                                 pv_charge='TORO:GUNB:360:CHRG', start=timestamps['start'],
                                                 end=timestamps['end'], charge_vals=charge_vals)


