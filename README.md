Podcast Transcription with AI
(Work in Progress)
---
# PodChat

PodChat is a Flask-based web application that automates the process of generating news articles from podcast episodes using AI. It fetches podcasts, transcribes audio, and creates engaging articles in a pop culture style.

## Features
- Search and retrieve podcast episodes using the Podcast Index API.
- Download and split podcast audio into chunks.
- Transcribe audio using OpenAI's Whisper API.
- Generate a news article summary with GPT in a fun, gossip-style tone.
- Display podcast details and articles via a web interface.

## Technologies Used
- **Backend:** Python, Flask, Requests, Pydub, OpenAI API
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **External Services:** Podcast Index API, OpenAI Whisper & GPT, ffmpeg (for audio processing)

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <project-directory>
   
2. Clone the repository:
   ```sh
   pip install flask openai pydub requests

3. Install and configure ffmpeg:
- Download from ffmpeg.org
- Set the correct path in app.py:
  ```sh
  AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"

4. Update API keys in config.py (or set them as environment variables).

## Running the App
Start the Flask server with:
  ```sh
python app.py
```
Visit http://127.0.0.1:5000 in your browser.

## Usage
- Open the webpage and the latest podcast episode will be processed.
- View the podcast details and generated article.
- Customize the podcast search query in app.py.

## Future Improvements
- Enhanced error handling and UI improvements.
- User-defined podcast searches.
- Deployment via Docker.

## License
This project is licensed under the MIT License.




