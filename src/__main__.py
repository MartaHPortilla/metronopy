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
    # Domain configuration
    bpm = 120
    number_of_bars = 16
    metronome = Metronome(bpm=bpm, number_of_bars=number_of_bars) # Example parameters

    # Infrastructure builders
    audio_builder = AudioBuilder(
        downbeat_sound_path="assets/audio/downbeat.wav",
        accent_sound_path="assets/audio/accent.wav",
        regular_sound_path="assets/audio/regular.wav"
    )

    video_builder = VideoBuilder(
        beat1_image_path="assets/images/beat1.png",
        beat2_image_path="assets/images/beat2.png",
        beat3_image_path="assets/images/beat3.png",
        beat4_image_path="assets/images/beat4.png"
    )

    # Composition
    composer = Composer(metronome=metronome, audio_builder=audio_builder, video_builder=video_builder)
    final_video = composer.compose()

    # Export 
    output_path = f"output/final/final_metronome_video_{bpm}_bpm_{number_of_bars}_bars.mp4"
    final_video.write_videofile(output_path, fps=video_builder.fps, audio_codec="aac", audio_fps=44100, audio_nbytes=2)
    print(f"Final video exported to {output_path}")

    # Cleanup 
    final_video.audio.close()
    final_video.close()
    if hasattr(final_video, '_temp_audio_path'):
        os.remove(final_video._temp_audio_path)

if __name__ == "__main__":
    main()