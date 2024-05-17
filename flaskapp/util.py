from openai_util import transcribe
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

import os
import subprocess

load_dotenv()


def getTranscript():
    print("getTranscript Called")
    try:
        print("attempting transcription")
        transcription = transcribe(os.environ["AUDIO_PATH"])
        with open(os.environ["TRANSCRIPT_PATH"], 'w') as file:
            file.write(transcription)
    except OSError as e:
        print('Access-error on file "'
              + os.environ["TRANSCRIPT_PATH"]
              + 'or' + os.environ["AUDIO_PATH"]
              + '"! \n' + str(e))
    if os.path.exists(os.environ["TRANSCRIPT_PATH"]):
        with open(os.environ["TRANSCRIPT_PATH"], 'r') as file:
            transcription = file.read()
        return transcription


def extract_audio(video_file, audio_file):
    """Extract audio from a video file and save it as an audio file."""
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file)
        print(f"Audio extracted and saved to {audio_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_to_mp4(input_file, output_file):
    """Convert a video file to mp4 format."""
    try:
        removeFile(output_file)
        command = [os.environ["FFMPEG_PATH"], '-i', input_file, output_file]
        subprocess.run(command, check=True)
        removeFile(input_file)
        print(f"File converted to mp4 and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def removeFile(filepath="test"):
    if os.path.exists(filepath):
        os.remove(filepath)
