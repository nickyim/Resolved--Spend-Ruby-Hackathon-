import os
import io
from dotenv import load_dotenv
import assemblyai as aai

from .parseComplaint import processComplaint

# load environment variables from .env file
load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def processAudio(file_path):
    print(f"\n\nReceived audio file: {file_path} \n\n ********")
    audio_file = file_path
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        print('ERROR:',transcript.error)
    else:
        print(f"\n\n******** Transcription: {transcript.text} ********\n\n")
        


    return processComplaint(transcript.text)
