import subprocess
import os
from save_to_database import save_voice


def convert(user_id, voice_path):
    convert_path = voice_path.replace(".oga", ".wav")
    subprocess.call('ffmpeg -i ' + str(voice_path) + ' -ar 16k ' + str(convert_path), shell=True)
    save_voice(user_id, convert_path)
    os.remove(voice_path)
