"""
Composer module.
    High-level orchestrator responsible for combining metronome-driven
    audio and video components into a synchronized final product (audiovisual clip).

    This class does not generate audio or video itself, but relies 
    on the builders and coordinates them based on the metronome's timing, 
    adapting their outputs when necessary.
"""

import os
import tempfile
from moviepy.editor import AudioFileClip
from moviepy.video.VideoClip import VideoClip
from beat import Beat
from typing import List
from pydub import AudioSegment
from metronome import Metronome
from audio_builder import AudioBuilder
from video_builder import VideoBuilder

class Composer:
    def __init__(self, metronome: Metronome, audio_builder: AudioBuilder, video_builder: VideoBuilder):
        self.metronome = metronome
        self.audio_builder = audio_builder
        self.video_builder = video_builder

    def compose(self) -> VideoClip:
        """
        Builds a fully synchronized audiovisual clip based on the current metronome.

        This method does not write any files to disk. It returns a MoviePy VideoClip
        ready to be exported by the caller (e.g. main or a UI layer).

        Returns final video clip with audio attached.
        """
        # Generate beat sequence calling metronome function
        beats = self.metronome.build_beat_sequence()

        # Build audio (pydub AudioSegment)
        audio_segment = self._generate_audio_segment(beats)
        
        # Export AudioSegment to a temporary wav file
        audio_path = self._generate_temp_audio_file_and_path(audio_segment)

        
        # Build video and combine with audio 
        video_clip = self._generate_video_clip(beats)
        final_clip = self._attach_audio_to_video(video_clip, audio_path)
        final_clip._temp_audio_path = audio_path # store temp path for later cleanup
        return final_clip # REAL final audiovisual clip
       


    # ----- Helper Methods ----- #

    def _generate_temp_audio_file_and_path(self, audio_segment: AudioSegment) -> str:
        """
        Exports an AudioSegment to a temporary WAV file for MoviePy compatibility.

        Returns path to the temporary audio file.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file: #False to keep for MoviePy usage
            audio_path = temp_audio_file.name
            audio_segment.export(audio_path, format="wav")
        return audio_path

    def _generate_audio_segment(self, beats: List[Beat]) -> AudioSegment: #add type hint
        """
        Creates and post-processes the audio segment based on beat timing.
        """
        audio_segment = self.audio_builder.build_audio_track(beats)
        audio_segment = audio_segment.normalize() # audio levels
        audio_segment = audio_segment.set_channels(1) # mono
        return audio_segment

    def _generate_video_clip(self, beats: List[Beat]) -> VideoClip:
        """
        Builds the silent video clip based on beat timing.
        """
        silent_video_clip = self.video_builder.build_video_track(beats=beats, metronome=self.metronome)
        return silent_video_clip

    def _attach_audio_to_video(self, silent_video_clip: VideoClip, audio_path: str) -> VideoClip:
        """
        Attaches audio to video and ensures synchronization.
        """
        audio_clip = AudioFileClip(audio_path)
        audio_clip = audio_clip.set_fps(44100)
        return silent_video_clip.set_audio(audio_clip)
   
    def _cleanup_temp_files(self, audio_path: str) -> None:
        """
        Removes temporary files created during composition.
        """
        if os.path.exists(audio_path):
            os.remove(audio_path)
