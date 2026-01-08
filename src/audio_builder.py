"""
AudioBuilder module.
    Responsible for generating a complete audio track based on a sequence
    of Beat objects, placing audio samples at precise timestamps.
"""

from beat import Beat
from beat_type import BeatType
from pydub import AudioSegment


class AudioBuilder:
    def __init__(self, downbeat_sound_path: str, accent_sound_path: str, regular_sound_path: str):
        self.downbeat_sound_path = downbeat_sound_path
        self.accent_sound_path = accent_sound_path
        self.regular_sound_path = regular_sound_path


    def build_audio_track(self, beats: list[Beat]) -> AudioSegment:
        """
        Builds a complete audio track by overlaying beat sounds
        at their corresponding timestamps.
        """
        # guard clause against empty beats sequence
        if not beats:
            raise ValueError("Beats list cannot be empty")
        
        # Determine total duration IN MILLISECONDS adding a buffer
        last_beat = beats[-1]
        BUFFER_MS = 1000
        total_duration_ms = int(last_beat.start_time * 1000) + BUFFER_MS

        # Create silent base track
        audio_track = AudioSegment.silent(duration=total_duration_ms)

        # Place each beat sound at the correct timestamp
        for beat in beats:
            sound_path = self._get_sound_path_for_beat(beat.beat_type)
            beat_sound = AudioSegment.from_wav(sound_path)
            position_ms = int(beat.start_time * 1000)
            audio_track = audio_track.overlay(beat_sound, position=position_ms)

        return audio_track


    def _get_sound_path_for_beat(self, beat_type: BeatType) -> str:
        """
        Returns the sound file path corresponding to the beat type.
        """
        if beat_type == BeatType.DOWNBEAT:
            return self.downbeat_sound_path
        elif beat_type == BeatType.ACCENT:
            return self.accent_sound_path
        elif beat_type == BeatType.REGULAR:
            return self.regular_sound_path
        else:
            raise ValueError(f"Invalid beat_type: {beat_type}")