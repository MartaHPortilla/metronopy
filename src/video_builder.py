"""
VideoBuilder module
    Responsible for generating a complete video track based on a sequence
    of Beat objects, placing image clips at precise timestamps.
"""

from beat import Beat
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.video.VideoClip import VideoClip

class VideoBuilder:
    def __init__(
        self, 
        beat1_image_path: str, 
        beat2_image_path: str, 
        beat3_image_path: str, 
        beat4_image_path: str,
        fps: int
    ):
        
        if not isinstance(fps, int) or fps <= 0:
            raise ValueError("FPS must be a positive integer")
        
        # Initialize the video builder with assets and video settings.
        self.beat_image_paths = {
            1: beat1_image_path,
            2: beat2_image_path,
            3: beat3_image_path,
            4: beat4_image_path
        }

        self.fps = fps 

    def build_video_track(self, beats: list[Beat], seconds_per_beat: float) -> VideoClip: 
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
                .set_duration(seconds_per_beat)
                .set_fps(self.fps)
            )
            clips.append(clip)

        silent_video_track: VideoClip = concatenate_videoclips(clips, method="chain")
        return silent_video_track

    def _get_image_path_for_beat(self, position_in_bar: int) -> str:
        """
        Returns the image path corresponding to the beat's position.
        """
        try:
            return self.beat_image_paths[position_in_bar]
        except KeyError:
            raise ValueError(f"No image configured for beat position {position_in_bar}.")