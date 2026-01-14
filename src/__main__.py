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
    # Configuration
    fps: int = 30
    bpm: int = 140
    #number_of_bars OR target_duration_seconds
    number_of_bars: int = 32
    target_duration_seconds: float = 300.0

    # Domain component
    #metronome = Metronome(bpm=bpm, number_of_bars=number_of_bars) # Example parameters
    # If using duration instead of bars:
    metronome2 = Metronome(bpm=bpm, target_duration_seconds=target_duration_seconds)

    # Builders
    audio_builder = AudioBuilder(
        downbeat_sound_path="assets/audio/downbeat.wav",
        accent_sound_path="assets/audio/accent.wav",
        regular_sound_path="assets/audio/regular.wav"
    )

    video_builder = VideoBuilder(
        beat1_image_path="assets/_legacy/metronomo1_140bpm.png",
        beat2_image_path="assets/_legacy/metronomo2_140bpm.png",
        beat3_image_path="assets/_legacy/metronomo3_140bpm.png",
        beat4_image_path="assets/_legacy/metronomo4_140bpm.png",
        fps=fps
    )

    # Composition
    composer = Composer(
        metronome=metronome2, 
        audio_builder=audio_builder, 
        video_builder=video_builder
    )
    final_video = composer.compose()

    # Export TODO extract to a function/module
    output_dir = "output/final"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"final_metronome_video_{bpm}_bpm_{int(metronome2.total_duration_seconds)}_seconds.mp4")
    final_video.write_videofile(
        output_path, 
        fps=video_builder.fps, 
        audio_codec="aac", 
        audio_fps=44100, 
        audio_nbytes=2)    
    print(f"Final video exported to {output_path}")

    # Cleanup
    if final_video.audio: # TODO: revisar si es necesario
        final_video.audio.close()
    final_video.close()
    composer.cleanup()

if __name__ == "__main__":
    main()