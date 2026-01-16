"""
Entry point of the application.

Responsibilities:
- Instantiate core domain components (Metronome)
- Configure infrastructure builders (AudioBuilder, VideoBuilder)
- Delegate composition to the Composer
- Export the final audiovisual metronome video
- Clean up temporary resources

This module contains no domain logic.
It only wires components together and triggers the process.
"""

import os
from metronome import Metronome
from audio_builder import AudioBuilder
from video_builder import VideoBuilder
from composer import Composer

def main():
    """
    Creates and configures all required components,
    triggers the composition process and exports
    the final metronome video to disk.
    """
    # --- Configuration ---
    fps: int = 30
    bpm: int = 140

    #number_of_bars OR target_duration_seconds
    number_of_bars: int = 32
    target_duration_seconds: float = 300.0

    # --- Domain component ---

    # using number of bars
    metronome_bars = Metronome(bpm=bpm, number_of_bars=number_of_bars) 
    # If using duration instead of bars:
    metronome_duration = Metronome(bpm=bpm, target_duration_seconds=target_duration_seconds)

    # --- Builders ---
    audio_builder = AudioBuilder(
        downbeat_sound_path="assets/audio/downbeat.wav",
        accent_sound_path="assets/audio/accent.wav",
        regular_sound_path="assets/audio/regular.wav"
    )

    video_builder = VideoBuilder(
        beat1_image_path="assets/images/beat1.png",
        beat2_image_path="assets/images/beat2.png",
        beat3_image_path="assets/images/beat3.png",
        beat4_image_path="assets/images/beat4.png",
        fps=fps
    )

    #  --- Composition ---
    composer = Composer(
        metronome=metronome_duration, 
        audio_builder=audio_builder, 
        video_builder=video_builder
    )
    final_video = composer.compose()

    # --- Export ---                                TODO extract to a function/module
    output_dir = "output/final"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"final_metronome_video_{bpm}_bpm.mp4")
    final_video.write_videofile(
        output_path, 
        fps=video_builder.fps, 
        audio_codec="aac", 
        audio_fps=44100, 
        audio_nbytes=2)    
    print(f"Final video exported to {output_path}")

    # --- Cleanup ---
    if final_video.audio:
        final_video.audio.close()
    final_video.close()
    composer.cleanup()

if __name__ == "__main__":
    main()