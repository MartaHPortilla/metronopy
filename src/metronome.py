import math
from beat_type import BeatType
from beat import Beat


class Metronome:
    """
    Represents a metronome configuration and provides methods to compute beat timings and types.
    - bpm: beats per minute (tempo)
    - beats_per_bar: number of beats per bar (time signature)
    - Total musical duration can be specified in one of two ways:
        - number_of_bars: total number of bars in the sequence
        - target_duration_seconds: total duration of the sequence in seconds
          When using target_duration_seconds the actual duration may be slightly longer to preserve full bars.
    """
    def __init__(
        self, 
        *, # Enforce keyword arguments for clarity
        bpm: int, 
        beats_per_bar: int = 4, 
        number_of_bars: int | None = None, 
        target_duration_seconds: float | None = None
    ):
        
        self._validate_parameters(
            bpm,
            beats_per_bar,
            number_of_bars,
            target_duration_seconds
        )
                    
        # Base state assignment
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar

        # Resolve total beats (number_of_bars OR target_duration_seconds)
        self._total_beats = self._resolve_total_beats(
            number_of_bars,
            target_duration_seconds
        )


    # --- Properties ---
    @property
    def total_beats(self) -> int:
        """
        Total number of beats in the full metronome sequence.
        """
        return self._total_beats 

    @property
    def seconds_per_beat(self) -> float:
        """
        Duration of a single beat in seconds.
        """
        return 60.0 / self.bpm
        
    @property
    def seconds_per_bar(self) -> float:
        """
        Duration of a single bar in seconds.
        """
        return self.seconds_per_beat * self.beats_per_bar
        
    @property
    def total_duration_seconds(self) -> float:
        """
        Total duration of the metronome sequence in seconds.
        """
        return self.total_beats * self.seconds_per_beat
    

    # --- Beat Type Determination ---

    def get_beat_type(self, beat_index: int) -> BeatType: 
        """
        Returns the beat type for a given beat index (0-based).

        Current behavior only assumes a 4/4 time signature:
        - Downbeat (1st beat of the bar): BeatType.DOWNBEAT
        - Accent (3rd beat of the bar): BeatType.ACCENT
        - Regular (2nd and 4th beats of the bar): BeatType.REGULAR
        The function can be extended for other time signatures in the future.
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
        Generates the full sequence of beats objects for the configured metronome.

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
    
    # --- Internal Helper Methods ---


    # Validators
    def _validate_parameters(
        self,
        bpm: int,
        beats_per_bar: int,
        number_of_bars: int | None,
        target_duration_seconds: float | None
    ) -> None:
        """
        Validates initialization parameters.
        """

        if bpm <= 0:
            raise ValueError("BPM must be greater than 0")
        if beats_per_bar <= 0:
            raise ValueError("Beats per bar must be greater than 0")
        if number_of_bars is not None and number_of_bars <= 0:
            raise ValueError("Number of bars must be greater than 0")
        if target_duration_seconds is not None and target_duration_seconds <= 0:
            raise ValueError("Target duration in seconds must be greater than 0")
        
        # Exclusivity validation
        if (number_of_bars is None) == (target_duration_seconds is None):
            raise ValueError("You must specify exactly one of the arguments: number of bars or target duration seconds")
 

    # Total beats calculators


    def _resolve_total_beats( self, number_of_bars: int | None, target_duration_seconds: float | None ) -> int:
        """
        Resolves the total number of beats needed based on either number of bars or target duration.
        """
        # Given number of bars
        if number_of_bars is not None:
            resolved_beats = self._resolve_beats_from_bars(number_of_bars)
            return resolved_beats

        # Given target duration in seconds
        minimum_beats = self._calculate_minimum_beats_from_duration(
            target_duration_seconds
        )
        
        resolved_beats = self._resolve_rounded_beats_to_complete_bars(minimum_beats)
        return resolved_beats
    
    def _resolve_beats_from_bars(self, number_of_bars: int) -> int:
        """
        Calculates the minimum number of beats based on a given number of bars.
        """
        return number_of_bars * self.beats_per_bar # e.g. 4 bars * 4 beats/bar = 16 beats

    def _calculate_minimum_beats_from_duration(self, target_duration_seconds: float) -> int:
        """
        Calculates the minimum number of beats based on a target duration.
        This may result in a number of beats that does not complete full bars.
        """
        return math.ceil(target_duration_seconds / self.seconds_per_beat)


    def _resolve_rounded_beats_to_complete_bars(self, minimum_beats: int) -> int:
        """
        Rounds up the total beats to ensure full bars.
        Returns the adjusted total beats.
        """
        remainder = minimum_beats % self.beats_per_bar
        if remainder == 0:
            return minimum_beats
        else:
            rounded_beats = minimum_beats + (self.beats_per_bar - remainder)
            return rounded_beats
        



