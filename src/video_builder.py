"""
AudioBuilder module
    Responsible for generating a complete video track based on a sequence
    of Beat objects, placing image clips at precise timestamps.
"""

from beat import Beat
from metronome import Metronome
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.video.VideoClip import VideoClip

class VideoBuilder:
    def __init__(
            self, 
            beat1_image_path: str, 
            beat2_image_path: str, 
            beat3_image_path: str, 
            beat4_image_path: str,
            fps: int = 30
    ):
        """
        Initializes the video builder with basic assets and basic video settings.
        """
        self.beat1_image_path = beat1_image_path
        self.beat2_image_path = beat2_image_path
        self.beat3_image_path = beat3_image_path
        self.beat4_image_path = beat4_image_path
        self.fps = fps

    def build_video_track(self, beats: list[Beat], metronome: Metronome) -> VideoClip:
        """
        Builds and returns a silent video track where each beat is represented by an image clip
        with precise duration derived from the metronome.
        """
        if not beats:
            raise ValueError("Beats list cannot be empty")

        clips: list[VideoClip] = []

        for beat in beats:
            image_path = self._get_image_path_for_beat(beat.position_in_bar)
            clip = (
                ImageClip(image_path)
                .set_duration(metronome.seconds_per_beat)
                .set_fps(self.fps)
            )
            clips.append(clip)

        silent_video_track: VideoClip = concatenate_videoclips(clips, method="chain")
        return silent_video_track

    def _get_image_path_for_beat(self, position_in_bar: int) -> str:
        """
        Returns the image path corresponding to the beat's position (1-4).
        """
        if position_in_bar == 1:
            return self.beat1_image_path
        elif position_in_bar == 2:
            return self.beat2_image_path
        elif position_in_bar == 3:
            return self.beat3_image_path
        elif position_in_bar == 4:
            return self.beat4_image_path
        else:
            raise ValueError(f"Invalid position_in_bar: {position_in_bar}. Must be 1-4.")