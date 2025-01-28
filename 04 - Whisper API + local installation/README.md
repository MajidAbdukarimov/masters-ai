# Audio to Text Transcription using Whisper

This project uses the [Whisper](https://github.com/openai/whisper) model by OpenAI to transcribe audio files into text and saves the transcriptions into a `.txt` file. It leverages the `pydub` library for audio processing and the Whisper model for transcription.

## Requirements

- Python 3.7+
- Required libraries:
  - `pydub`
  - `whisper`
  - `ffmpeg` (for audio file conversion)
  
You can install the required Python libraries by running:

```bash
pip install pydub whisper
