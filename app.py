import sounddevice as sd
from scipy.io.wavfile import write
import requests
import os
import string  # ✅ Needed for punctuation cleanup
import modules.llm_engine as llm_engine
import modules.music as music  # ✅ Existing music integration
import modules.weather as weather  # ✅ New: Weather integration

# Create an output directory if it doesn't exist
output_dir = "recordings"
os.makedirs(output_dir, exist_ok=True)

def record_audio(sample_rate=44100, duration=5, output_file="output.wav"):
    output_file = os.path.join(output_dir, output_file)
    print("Recording...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    print("Recording finished. Saving to file...")
    write(output_file, sample_rate, audio_data)
    print(f"Audio saved to {output_file}")

def make_asr_request(audio_file):
    try:
        base_url = 'http://localhost:9000'
        with open(audio_file, 'rb') as f:
            file = {'audio_file': f}
            r = requests.post(f'{base_url}/asr?task=transcribe&language=en&encode=true&output=json', files=file)
        return r.json()['text']
    except requests.exceptions.ConnectionError:
        return "Offline"

# ✅ Music command handler
def handle_music_command(command):
    if "play" in command and "on spotify" in command:
        query = command.replace("play", "").replace("on spotify", "").strip()
        print(music.play_on_spotify(query))
        return True
    elif "pause spotify" in command:
        print(music.pause_spotify())
        return True
    elif "resume spotify" in command:
        print(music.resume_spotify())
        return True
    elif "next song" in command or "next track" in command:
        print(music.next_spotify())
        return True
    elif "play" in command and "on youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        print(music.play_on_youtube(query))
        return True
    return False

# ✅ Weather command handler (newly added)
def handle_weather_command(command):
    keywords = ["weather", "temperature", "forecast", "how hot", "how cold", "humidity"]
    if any(kw in command for kw in keywords):
        city = "hyderabad"
        if " in " in command:
            parts = command.split(" in ")
            if len(parts) > 1:
                city = parts[1].strip().split()[0].strip(string.punctuation)
        print(weather.get_weather(city))
        return True
    return False

def main():
    try:
        record_audio()
        transcript = make_asr_request(os.path.join(output_dir, "output.wav"))
        print(f"📝 Transcript: {transcript}")

        if handle_music_command(transcript.lower()):
            return

        if handle_weather_command(transcript.lower()):
            return

        llm_engine.ollama_wrapper(transcript)

    except Exception as e:
        print("An error occurred during the process:", e)
        input("Press Enter to exit\n")

