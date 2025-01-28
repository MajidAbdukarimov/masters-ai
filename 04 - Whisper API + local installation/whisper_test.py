from pydub import AudioSegment
import whisper

# Load Whisper model
model = whisper.load_model("base")

# Transcribe the extracted segment
result = model.transcribe("ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording.mp3")

# Print or save the transcription
print(result["text"])
with open("transcription.txt", "w") as f:
    f.write(result["text"])