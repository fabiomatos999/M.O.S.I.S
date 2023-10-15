from enum import Enum


class shotType(Enum):
    """Shot Type for the type of study to be performed."""

    SINGLE = 1
    BURST = 2
    TELESCOPIC = 3
    TIMELAPSE = 4
    VIDEO = 5


class illuminationType(Enum):
    """Illumination Type."""

    NONE = 1
    WHITE = 2
    RED = 3
    ULTRAVIOLET = 4
