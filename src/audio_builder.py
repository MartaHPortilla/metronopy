"""
AudioBuilder module.
    Responsible for generating a complete, fully processed audio track based 
    on a sequence of Beat objects. The resulting AudioSegment contains:
        - Deterministic duration, 
        - Guaranteed sample rate
        - Channel configuration. 
    It produces a polished audio output ready for synchronization without further processing.
"""

from beat import Beat
from beat_type import BeatType
from pydub import AudioSegment


class AudioBuilder:
    def __init__(
        self,
        downbeat_sound_path: str, 
        accent_sound_path: str, 
        regular_sound_path: str,
        sample_rate: int = 44100,
        channels: int = 1,
    ):
        self.sample_rate = sample_rate
        self.channels = channels

        # Load and normalize beat sounds 
        self.downbeat_sound = self._load_sound(downbeat_sound_path)
        self.accent_sound = self._load_sound(accent_sound_path)
        self.regular_sound = self._load_sound(regular_sound_path)


    def build_audio_track(self, beats: list[Beat]) -> AudioSegment: 
        """
        Builds a complete audio track by overlaying beat sounds
        at their corresponding timestamps.

        The returned AudioSegment:
        - has a duration equal to the end of the last beat sound
        - has a fixed sample rate and channel count
        - is fully postprocessed and ready for export
        """
        # guard clause against empty beats sequence
        if not beats:
            raise ValueError("Beats list cannot be empty")
        
        # Determine total duration 
        total_duration_ms = self._calculate_total_duration_ms(beats)

        # Create silent base track
        audio_track = AudioSegment.silent(
            duration=total_duration_ms, 
            frame_rate=self.sample_rate
        ).set_channels(self.channels) #dos veces?

        # Place each beat sound at the correct timestamp
        for beat in beats:
            beat_sound = self._get_sound_for_beat(beat.beat_type)
            position_ms = int(beat.start_time * 1000)
            audio_track = audio_track.overlay(beat_sound, position=position_ms)

        return self._postprocess(audio_track)

    # Helper internal methods

    def _load_sound(self, path: str) -> AudioSegment:
        """
        Loads a WAV file and enforces sample rate and channel count.
        """
        sound = AudioSegment.from_wav(path)
        sound = sound.set_frame_rate(self.sample_rate)
        sound = sound.set_channels(self.channels)
        return sound

    def _get_sound_for_beat(self, beat_type: BeatType) -> AudioSegment:
        """
        Returns the AudioSegment corresponding to the beat type.
        """
        if beat_type == BeatType.DOWNBEAT:
            return self.downbeat_sound
        elif beat_type == BeatType.ACCENT:
            return self.accent_sound
        elif beat_type == BeatType.REGULAR:
            return self.regular_sound
        else:
            raise ValueError(f"Invalid beat_type: {beat_type}")
        
    def _calculate_total_duration_ms(self, beats: list[Beat]) -> int:
        """
        Calculates the exact duration needed to contain all beat sounds.
        """
        max_end_time = 0.0

        for beat in beats:
            sound = self._get_sound_for_beat(beat.beat_type)
            sound_duration_sec = sound.duration_seconds
            beat_end_time = beat.start_time + sound_duration_sec
            max_end_time = max(max_end_time, beat_end_time)

        return int(max_end_time * 1000)
    
    def _postprocess(self, audio: AudioSegment) -> AudioSegment:
        """
        Applies final processing steps to the audio track.
        Currently applies normalization.
        """
        return audio.normalize()
        
