from enum import Enum, verify, UNIQUE, CONTINUOUS


@verify(UNIQUE, CONTINUOUS)
class shotType(Enum):
    """Shot Type for the type of study to be performed."""

    SINGLE = 1
    BURST = 2
    TELESCOPIC = 3
    TIMELAPSE = 4
    VIDEO = 5


@verify(UNIQUE, CONTINUOUS)
class illuminationType(Enum):
    """Illumination Type."""

    NONE = 1
    VISIBLESPECTRUM = 2
    INFRARED = 3
    ULTRAVIOLET = 4
