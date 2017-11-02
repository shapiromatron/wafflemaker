"""Constants in the library."""
from enum import Enum


class CellFillDirection(Enum):
    # From top-left to bottom-right, filling by column.
    # From bottom-left to top-right, filling by row.
    ByColumn = 1
    ByRow = 2
