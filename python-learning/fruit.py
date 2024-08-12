from typing import Annotated, Dict, List, Literal, Tuple

from annotated_types import Gt

from pydantic import BaseModel

"""Demonstrates the different types that Pydantic supports when creating objects. Demonstrates strict mode that does not
automatically coerce data to the correct type.
"""


class Fruit(BaseModel):
    name: str
    color: Literal["red", "green", "blue"]  # enforces color to only be set to these specific Literals
    weight: Annotated[float, Gt(0)]  # this requires the float value to be greater than 0, using the Annotated type
    bazam: Dict[str, List[Tuple[int, bool, float]]]  # arbitrarily complex types can be checked


# Create a model with the correct types and print the object's parameters and values
print(
    Fruit(
        name="Apple",
        color="red",
        weight=0.5,
        bazam={"random": [(1, False, 0.5)]}
    )
)

# To create a model that follows strict typing, use the model_validate function and pass in the parameters
my_fruit = Fruit.model_validate({"name": "Apple",
                                 "color": "red",
                                 "weight": "0.5",
                                 "bazam": {"random": [(1, False, 0.5)]}},
                                strict=True)
