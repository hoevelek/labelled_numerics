from .geometry import Line, Point
from .roman_numbers import RomanNumbers
from .utils.labelled_numerics import LabelledNumerics
from .utils_geometry import distance

__all__ = [
    "Line",
    "Point",
    "distance",
    "LabelledNumerics",
    "RomanNumbers",
]  # API

__version__ = "0.8.0"  # version of package


def personal_message():
    print("Hello from John Doe!")
