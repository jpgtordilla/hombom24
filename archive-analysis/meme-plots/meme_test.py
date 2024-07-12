# COPY THIS FILE INTO SLAC DIRECTORY

import meme.archive # type: ignore
from datetime import datetime

# Goal: comparing MEME to lcls-tools -> returning a list of values

# both use datetime objects 
start_date = "2024/07/02 14:42:36"
end_date = "2024/07/02 15:42:36" 
format_string = "%Y/%m/%d %H:%M:%S"
start_date_obj = datetime.strptime(start_date, format_string)
end_date_obj = datetime.strptime(end_date, format_string)

# MEME
meme_data = meme.archive.get(["TORO:GUNB:360:CHRG"], from_time=start_date_obj, to_time=end_date_obj)

# TODO: compare data from MEME with lcls-tools
print(meme_data) # get an idea of its format
print(type(meme_data))