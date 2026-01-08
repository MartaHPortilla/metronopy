"""
📌 Este archivo contendrá:
- la clase Metronome
- BPM, compás, compases
- duraciones y tiempos exactos
👉 Todo lo demás dependerá de esto, nunca al revés.
"""

from beat_type import BeatType
from beat import Beat


class Metronome:
    """
    Represents a metronome configuration and provides methods to compute beat timings and types.
    - bpm: beats per minute
    - number_of_bars: total number of bars in the sequence
    """
    def __init__(self, bpm: int, number_of_bars: int):
        # Validations
        if bpm <= 0:
            raise ValueError("BPM must be greater than 0")
        if number_of_bars <= 0:
            raise ValueError("Number of bars must be greater than 0")
            
        # State
        self.bpm = bpm
        self.number_of_bars = number_of_bars

        # Domain constant - assuming 4/4 time signature
        self.beats_per_bar = 4

    @property
    def seconds_per_beat(self) -> float:
        """
        Duration of a single beat in seconds.
        """
        return 60.0 / self.bpm
        
    @property
    def seconds_per_bar(self) -> float:
        """
        Duration of a single bar (4/4) in seconds.
        """
        return self.seconds_per_beat * self.beats_per_bar
        
    @property
    def total_beats(self) -> int:
        """
        Total number of beats in the metronome sequence.
        """
        return self.number_of_bars * self.beats_per_bar      

    @property
    def total_duration_seconds(self) -> float:
        """
        Total duration of the metronome in seconds.
        """
        return self.seconds_per_bar * self.number_of_bars
    

    # --- Beat Type Determination ---

    def get_beat_type(self, beat_index: int) -> BeatType: 
        """
        Returns the BeatType for a given beat index (0-based).
        """
        position_in_bar = beat_index % self.beats_per_bar 

        if position_in_bar == 0:
            return BeatType.DOWNBEAT
        elif position_in_bar == 2:
            return BeatType.ACCENT
        else:
            return BeatType.REGULAR


    # --- Beat list Generation ---

    def build_beat_sequence(self) -> list[Beat]:
        """
        Generates the full sequence of beats for the configured metronome.

        Each Beat contains:
        - global index
        - position within the bar (1-4)
        - beat type (DOWNBEAT, ACCENT, REGULAR)
        - absolute start time in seconds
        """
        beats: list[Beat] = []
        for i in range(self.total_beats):
            position_in_bar = (i % self.beats_per_bar) + 1
            beat_type = self.get_beat_type(i)
            start_time = i * self.seconds_per_beat

            beats.append(Beat(index=i, position_in_bar=position_in_bar, beat_type=beat_type, start_time=start_time))

        return beats