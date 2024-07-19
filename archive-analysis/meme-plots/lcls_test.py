import sys
sys.path.append('/Users/jonathontordilla/Desktop/hombom24/archive-analysis/lcls-tools-plots/lcls_tools')
import common.data_analysis.archiver as arch  # type: ignore
from datetime import datetime

"""Comparing lcls-tools to MEME -> logging a list of values"""

# both use datetime objects
start_date = "2024/07/02 14:42:36"
end_date = "2024/07/02 15:42:36"
format_string = "%Y/%m/%d %H:%M:%S"
start_date_obj = datetime.strptime(start_date, format_string)
end_date_obj = datetime.strptime(end_date, format_string)

# lcls-tools: get data from the PV TORO:GUNB:360:CHRG over a specific 1 hour period
lcls_data = arch.get_values_over_time_range(["TORO:GUNB:360:CHRG"], start_date_obj, end_date_obj)
lcls_timestamps = lcls_data["TORO:GUNB:360:CHRG"].timestamps
lcls_values = lcls_data["TORO:GUNB:360:CHRG"].values

# log values and timestamps
print(f"VALUES: \n {lcls_values}")
print(f"TIMESTAMPS: \n {lcls_timestamps}")
