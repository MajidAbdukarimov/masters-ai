# Audio Transcription Project

## Overview

This Python project enables precise audio transcription by extracting a specific segment from an audio file and converting it to text using the Whisper model.

## Features

- Extract targeted audio segments using precise time ranges
- Transcribe audio with high accuracy using OpenAI's Whisper model
- Save transcription results to a text file
- Support for various audio file formats

## Prerequisites

### System Requirements
- Python 3.6+
- FFmpeg or libav installed

### Dependencies
- pydub
- whisper

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/audio-transcription-project.git](https://github.com/MajidAbdukarimov/masters-ai/tree/main/04%20-%20Whisper%20API%20%2B%20local%20installation)
cd audio-transcription-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### FFmpeg Installation
- **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

## Project Structure
```
.
├── audio_transcription.py     # Main transcription script
├── requirements.txt           # Project dependencies
├── segment_output.mp3         # Extracted audio segment
├── transcription_result.txt   # Transcription output
└── README.md                  # Project documentation
```

## Usage

### Configure Audio Transcription
1. Update `audio_path` in `audio_transcription.py` with your audio file path
2. Set desired `start_ms` and `end_ms` for audio segment extraction

### Run the Script
```bash
python audio_transcription.py
```

## Troubleshooting
- Verify FFmpeg installation
- Check audio file path
- Confirm all dependencies are installed

## License
MIT License - See LICENSE file for details
