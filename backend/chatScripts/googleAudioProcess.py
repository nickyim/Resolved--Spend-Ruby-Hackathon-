import os
from google.cloud import speech
from .parseComplaint import processComplaint

# Transcribes the audio file specified by the source_uri.
def transcribe_audio(audio_content, encoding):
    # Create a Speech Client object to interact with the Speech Client Library.
    client = speech.SpeechClient()

    # Create audio and config objects that you'll need to call the API.
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Call the Speech API using the Speech Client's recognize function.
    response = client.recognize(config=config, audio=audio)

    # Concatenate all transcripts
    full_transcript = " ".join([result.alternatives[0].transcript for result in response.results])

    return processComplaint(full_transcript)
