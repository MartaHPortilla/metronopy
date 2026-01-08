
from dataclasses import dataclass
from beat_type import BeatType

@dataclass(frozen=True)
class Beat:
    """
    Represents a single beat event in time.

    - index: global beat index (0-based) across the whole sequence
    - position_in_bar: beat position inside the bar (1..4 for 4/4)
    - beat_type: musical emphasis (DOWNBEAT, ACCENT, REGULAR)
    - start_time: exact time (in seconds) when the beat occurs
    """
    index: int
    position_in_bar: int
    beat_type: BeatType 
    start_time: float