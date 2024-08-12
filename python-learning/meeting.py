from datetime import datetime

from pydantic import BaseModel


"""Demonstrate Serialization: the process of initializing an object and outputting its parameters and values in a 
readable format.
"""


class Meeting(BaseModel):
    when: datetime
    where: bytes
    why: str = "No idea"


m = Meeting(when="2020-01-01T12:00", where="Home")

# Converting a model into a dictionary or json
print(m.model_dump(exclude_unset=True))  # leaves out parameters not set in declaration
print(m.model_dump(exclude={"where"}, mode="json"))  # excludes where parameter, formats datetime as a string for json
print(m.model_dump(exclude_defaults=True))  # leaves out parameters where defaults are set

# Converting a model exclusively to a json
print(m.model_dump_json())



