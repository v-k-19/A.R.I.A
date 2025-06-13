from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os
from pydub import AudioSegment
import sounddevice as sd
import numpy as np

def run(text):
    """
    Function to run the ElevenLabs text-to-speech synthesis.
    """

    def play_audio_file(filename):
        # Direct playback if file exists
        if os.path.exists(filename):
            if filename.endswith('.mp3'):
                sound = AudioSegment.from_mp3(filename)
            elif filename.endswith('.wav'):
                sound = AudioSegment.from_wav(filename)
            else:
                return  # Unsupported file format
            
            # Convert to numpy array for sounddevice
            audio_data = np.array(sound.get_array_of_samples())
            
            # Handle stereo audio
            if sound.channels == 2:
                audio_data = audio_data.reshape((-1, 2))
            
            # Play using sounddevice
            sd.play(audio_data, samplerate=sound.frame_rate)
            sd.wait()  # Wait until playback is finished

    # Your ElevenLabs API key
    api_key = "sk_bdc083b4ca9cad7c81483b6f42ee57fd8e85cfc9394306a6"  # Replace with your actual key

    # Set up the ElevenLabs client
    client = ElevenLabs(api_key=api_key)

    available_voices = client.voices.get_all()

    # Selecting Liam
    selected_voice = available_voices.voices[7]

    # Generate speech (returns a generator of audio chunks)
    audio = client.text_to_speech.convert(
        voice_id=selected_voice.voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    )

    # Create recordings directory if it doesn't exist
    os.makedirs("recordings", exist_ok=True)
    
    # Write audio to file in recordings directory
    output_path = os.path.join("recordings", "eleven_speak.mp3")
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    play_audio_file(output_path)
