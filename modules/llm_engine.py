import ollama
import json
import subprocess
import modules.tts_engine as tts_engine

ALLOWED_COMMANDS = [
    "systemctl",
    "reboot",
    "gnome-session-quit",
    "gnome-screensaver-command",
    "xdg-open",
    "hostname",
    "ping",
    "pwd",
    "ls",
    "mkdir",
    "rm",
    "df",
    "find",
    "gnome-terminal",
    "gedit",
    "nautilus",
    "gnome-system-monitor",
    "vlc",
    "amixer",
    "cal",
    "date",
    "gnome-screenshot",
    "curl"
]

def is_valid_command(cmd: str):
    return any(cmd.startswith(allowed) for allowed in ALLOWED_COMMANDS)

def sanitize_json_block(raw: str) -> str:
    """Remove markdown-style ```json wrappers from the response."""
    lines = raw.strip().splitlines()
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def ollama_wrapper(transcript):
    response = ollama.chat(
        model="AriaBot",  # Your custom model name
        messages=[
            {"role": "user", "content": transcript}
        ]
    )

    message = response['message'].get('content', '')
    json_candidate = sanitize_json_block(message)

    try:
        content_dict = json.loads(json_candidate)

        if "CMD" in content_dict:
            command = content_dict["CMD"]
            print(f"About to execute: {command}")
            try:
                user_input = input("Run this command? [y/N]: ").strip().lower()
                if user_input.startswith('y'):
                    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if result.stdout:
                        print("Output:\n", result.stdout)
                    if result.stderr:
                        print("Error:\n", result.stderr)
                else:
                    print(f"Command not executed. Command was: {command}")
                    return
            except KeyboardInterrupt:
                print(f"\nCommand not executed due to keyboard interrupt. Command was: {command}")

        elif "SAY" in content_dict:
            print("Assistant says:", content_dict["SAY"])
            tts_engine.run(content_dict["SAY"])

        else:
            print("Unrecognized JSON structure:", json_candidate)

    except json.JSONDecodeError as jde:
        print("Failed to parse JSON. Raw message was:\n", repr(json_candidate))
        print("JSONDecodeError:", jde)
    except Exception as e:
        print("An error occurred while parsing or executing:", e)
