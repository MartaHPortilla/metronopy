
from enum import Enum, auto

class BeatType(Enum):
    """
    Represents the type of a beat in a metronome sequence.   
    """
    DOWNBEAT = auto() # first beat of the bar
    ACCENT = auto() # typically the third beat in 4/4 time
    REGULAR = auto() # other beats
    