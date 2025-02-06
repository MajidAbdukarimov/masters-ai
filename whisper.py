from pydub import AudioSegment
import whisper

# Define the path for the audio file
audio_path = "ITPU_MS_Degree_Session_5_-_Generative_AI-20241213_153714-Meeting_Recording.mp3"

# Load the audio
audio_data = AudioSegment.from_file(audio_path)

# Set the time range for the clip (from 10 to 15 minutes)
start_ms = 15 * 60 * 1000  # Start time in milliseconds
end_ms = 18 * 60 * 1000    # End time in milliseconds

# Extract the audio segment
audio_snippet = audio_data[start_ms:end_ms]

# Save the segment as a new file
snippet_path = "segment_output.mp3"
audio_snippet.export(snippet_path, format="mp3")

# Initialize the Whisper model
whisper_model = whisper.load_model("base")

# Perform transcription on the segment
transcription = whisper_model.transcribe(snippet_path)

# Output the transcribed text and save it to a file
print(transcription['text'])
with open("transcription_result.txt", "w") as output_file:
    output_file.write(transcription['text'])
