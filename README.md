All code written during my time at SLAC as a Science Undergraduate Laboratory Intern during the summer of 2024. 

See the "CULMINATION" folder for the "final" scripts that are the culmination of dozens of scripts and notebooks written over a period of about 9 weeks. 

# Culmination Files
*archiver_data_process:* script that was merged into the wider lcls-tools repository, more or less. 
Creates PVModels (objects used to store data for a Process Variable, or PV) and DataFrames for plotting. 

*buncher_dates.html:* an HTML file downloaded from the LCLS-II logbook containing information for the buncher phase scans in early 2024. 
Dates for each logbook entry are pulled from this file and used to plot correlations over time during buncher phase scans
in the file: *generate_plots.py*. 

*charge_plotter.py:* plots charge-separated plots for correlations. This means that DataFrames containing a column for charge
data are filtered so that only charges within a specific range are included in the plotted data. Additional error calculations
and plot styling are also configured in this file. 

*charge_separator:* the actual script that creates clusters of charges given a dataset or separate DataFrames by charge. 

*generate_plots:* IMPORTANT script that actually plots the correlations. Set your own parameters at the bottom of the file.

*plotting_base:* script that was merged into the wider lcls-tools repository, more or less. A better-organized, more general 
script for plotting PVs over time and correlations between PVs. 

*plotting_example:* USEFUL script that teaches new users of this repository how to actually use the *plotting_base* and
*archiver_data_process* scripts.


