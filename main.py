from dantri import dantri_agent
import requests
from datetime import datetime
import logging
import os
import traceback

print('Script has been started at {}'.format(datetime.now()))

if __name__ == "__main__":
    try:
        audios = dantri_agent.get_current_audio_file()
        for item in audios:
            logging.info("Push audio file {}".format(item))
    except Exception as e:
        traceback.print_exc()

    