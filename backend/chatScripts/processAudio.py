import os
import io
from openai import OpenAI
from dotenv import load_dotenv
from .parseComplaint import processComplaint

# load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def processAudio(audioFile):
    audio_file = open('complaintUploads/userComplaint.mp3', 'rb')
    transcription = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
        response_format='text'
    )

    print(f"\n\n******** Transcription: {transcription}")

    return processComplaint(transcription)
