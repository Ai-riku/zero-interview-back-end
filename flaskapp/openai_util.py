from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

def prompt_to_text(prompt):
    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    params = {
        "model": "gpt-3.5-turbo",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 500,
    }

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.chat.completions.create(**params)
    print(result.choices[0].message.content)
    return result.choices[0].message.content

def transcribe(audio_path):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription.text)
    return transcription.text

if __name__=="__main__":
    transcribe()