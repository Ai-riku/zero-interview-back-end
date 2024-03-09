from av_util import video_capture
from openai_util import *

import config
import os
import time

transcription_complete = False

def interview():
    global transcription_complete
    yield from video_capture()
    try:
        print("attempting transcription")
        transcription = transcribe(config.audio_path)
        with open(config.transcript_path, 'w') as file:
            file.write(transcription)
    except OSError as e:
        print('Access-error on file "' + config.transcript_path + 'or' + config.audio_path + '"! \n' + str(e))
        time.sleep(1)
    print("transcription complete")
    transcription_complete = True

def getTranscript():
    print("getTranscript Called")
    if os.path.exists(config.transcript_path):
        with open(config.transcript_path, 'r') as file:
            transcription = file.read()
        return transcription

def audio_transcript_complete():
    return transcription_complete

def removeFile(filepath="test"):
    if os.path.exists(filepath):
        os.remove(filepath)