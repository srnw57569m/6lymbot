from importlib import import_module
from highrise.__main__ import *
import time
import traceback
import psutil

# BOT SETTINGS #
bot_file_name = "musicbot"
bot_class_name = "MyBot"
room_id = "696304510df902a35e522aa7"
bot_token = "6e7028c15394ab30991973799bb04f6e4b94227811e929b0cf27365ffb738bf6"

def terminate_ffmpeg_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'ffmpeg' in proc.info['name']:
            try:
                proc.terminate()
                print(f"Terminated FFmpeg process: {proc.info['pid']}")
            except Exception as e:
                print(f"Failed to terminate process {proc.info['pid']}: {e}")

my_bot = BotDefinition(getattr(import_module(bot_file_name), bot_class_name)(), room_id, bot_token)

while True:
    try:
        # Cleanup lingering FFmpeg processes before restarting
        terminate_ffmpeg_processes()

        definitions = [my_bot]
        arun(main(definitions))
    except Exception as e:
        print(f"An exception occurred: {e}")
        traceback.print_exc()
        
        # Delay before reconnect attempt
        time.sleep(5)
