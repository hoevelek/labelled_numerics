from .geometry import Line, Point
from .utils import distance

__all__ = [
    "Line",
    "Point",
    "distance",
]  # pretends of using it, it declares functions which would be imported if we use from mypackage.geometry import *

__version__ = "0.5.0"  # version of package


def personal_message():
    print("Hello from John Doe!")
