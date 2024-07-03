import sys
sys.path.append('/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools') # change to your path to lcls_tools
import common.data_analysis.archiver as arch # type: ignore
from datetime import datetime
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class LclsToolsPlotter(): 
    pass

# TODO: 
# - plot a single PV over time
# - megaplot given a list of PVs
# - filtering method that returns peaks of a single PV
# - filtering method that returns peaks of a list of PVs
# - filtering method that plots and returns peaks of a single PV
# - filtering method that plots and returns peaks of a list of PVs
# - plot a correlation betwen two PVs
# - megaplot a correlation between a PV and a list of PVs
# - HOM plots... 

