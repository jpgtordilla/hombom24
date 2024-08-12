from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError

"""https://docs.pydantic.dev/latest/#pydantic-examples

Demonstrate creating an object and setting parameters. Uses a dictionary to set parameters. Demonstrate error 
handling upon using incorrect types in parameters.
"""


class User(BaseModel):
    id: int
    name: str = "John Smith"
    signup_ts: datetime | None
    inventory: dict[str, PositiveInt]


jonathon_data = {
    "id": 1,
    "name": "Jonathon Tordilla",
    "signup_ts": "2024-08-09 13:12",
    "inventory": {
        "computer": 1,
        "pen": 2
    }
}

wrong_data = {
    "id": "not an integer",
    "name": 5
}

# create an object using a dictionary as parameters
jonathon_user = User(**jonathon_data)

# try to create an object with incorrect parameter types
wrong_user = User(**wrong_data)
