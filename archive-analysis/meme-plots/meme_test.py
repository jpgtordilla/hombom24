import meme.archive  # type: ignore
from datetime import datetime

"""Comparing MEME to lcls-tools -> logging a list of values"""

# both use datetime objects 
start_date = "2024/07/02 14:42:36"
end_date = "2024/07/02 15:42:36"
format_string = "%Y/%m/%d %H:%M:%S"
start_date_obj = datetime.strptime(start_date, format_string)
end_date_obj = datetime.strptime(end_date, format_string)

# MEME: get data from the PV TORO:GUNB:360:CHRG over a specific 1 hour period
meme_data = meme.archive.get(["TORO:GUNB:360:CHRG"], from_time=start_date_obj, to_time=end_date_obj)

# log data with the purpose of comparing to a potentially identical dataset retrieved from lcls-tools
print(f"TYPE: {type(meme_data)}")
print(f"DATA: {meme_data}")  # get an idea of its format
