import os
import pvporcupine
import sounddevice as sd
import app

ACCESS_KEY = "nCIp+hAItOhRCXVVpcG6mhftRiipb8eiVUoXapkanHWa0/NKZp+Wvw=="
KEYWORD_PATH = os.path.join(os.getcwd(), "assets", "hey-Aria_en_linux_v3_0_0.ppn")

def create_porcupine():
    return pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]
    )

def listen_for_wake_word():
    porcupine = create_porcupine()
    print("🎙️ Listening for custom wake word...")

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        pcm = indata[:, 0]
        pcm = (pcm * 32768).astype('int16')
        if porcupine.process(pcm) >= 0:
            print("✅ Wake word detected!")

            # Insert assistant activation code here
            app.main()

    try:
        with sd.InputStream(
            channels=1,
            samplerate=porcupine.sample_rate,
            blocksize=porcupine.frame_length,
            dtype='float32',
            callback=callback
        ):
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("🛑 Stopping...")
    finally:
        porcupine.delete()

if __name__ == "__main__":
    listen_for_wake_word()
