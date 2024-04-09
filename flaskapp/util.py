from av_util import video_capture
from openai_util import transcribe

import config
import os

transcription_complete = False


def interview():
    global transcription_complete
    yield from video_capture()
    try:
        print("attempting transcription")
        transcription = transcribe(config.AUDIO_PATH)
        with open(config.TRANSCRIPT_PATH, 'w') as file:
            file.write(transcription)
    except OSError as e:
        print('Access-error on file "'
              + config.TRANSCRIPT_PATH
              + 'or' + config.AUDIO_PATH
              + '"! \n' + str(e))
        return
    print("transcription complete")
    transcription_complete = True


def getTranscript():
    print("getTranscript Called")
    if os.path.exists(config.TRANSCRIPT_PATH):
        with open(config.TRANSCRIPT_PATH, 'r') as file:
            transcription = file.read()
        return transcription


def audio_transcript_complete():
    return transcription_complete


def removeFile(filepath="test"):
    if os.path.exists(filepath):
        os.remove(filepath)
