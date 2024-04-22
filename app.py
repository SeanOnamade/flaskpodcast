from flask import Flask, jsonify, render_template
import requests
from openai import OpenAI
import time
import hmac
import hashlib
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/generate_article")
def generate_article():
    # Podcast Index API credentials

    api_key = "in notes"
    api_secret = "in notes"
    current_time = str(int(time.time()))
    encoded_api_key = api_key.encode('utf-8')
    encoded_api_secret = api_secret.encode('utf-8')
    encoded_current_time = current_time.encode('utf-8')
    hash_input = encoded_api_key + encoded_api_secret + encoded_current_time
    
    # Construct the search query
    search_query = "Everybody's Crazy"
    search_url = f"https://api.podcastindex.org/api/1.0/search/byterm?q={search_query}"

    # Make the search request
    headers = {
        "X-Auth-Date": current_time,  # You may need to replace this with a valid timestamp
        "X-Auth-Key": api_key,
        "User-Agent": "podcaster",  # You may need to replace this with your user agent,
        "Authorization": hashlib.sha1(hash_input).hexdigest()
    }
    response = requests.get(search_url, headers=headers)
    json_response = response.json()
    if response.status_code == 200 and json_response.get('status') == 'true':
        # Extract feed ID from the search results
        feed_id = json_response['feeds'][0]['id']
        
        # Construct URL to fetch episodes
        episodes_url = f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={feed_id}"

        # Make request to fetch episodes
        episodes_response = requests.get(episodes_url, headers=headers)
        episodes_data = episodes_response.json()

        # Check if episodes were fetched successfully
        if episodes_response.status_code == 200 and episodes_data.get('status') == 'true' and episodes_data.get('count') > 0:
            most_recent_episode = episodes_data['items'][0]
            audio_url = most_recent_episode['enclosureUrl']

            # Download audio file
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                audio_file_path = 'speech.mp3'
                with open(audio_file_path, 'wb') as file:
                    file.write(audio_response.content)

                # Transcribe audio using OpenAI
                client = OpenAI(api_key="in notes")
                audio_file = open("speech.mp3", "rb")
                transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
                podcast_transcript = transcription.text

                # Prepare example article and style description
                example_article = """Your example article here"""
                style_description = "a pop culture media establishment that reveals news in a spilling the tea way"

                # Generate news article summary using OpenAI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "system",
                        "content": f"You are a teenage girl writing a news article on all the latest celeb drama and tea. Here is a transcript of a podcast:\n{podcast_transcript}\n\nI want to generate a news article summary in the style of the following example article:\n{example_article}\nThe style is characterized by {style_description}."
                    }, {
                        "role": "user",
                        "content": "Please generate a news article summary of the podcast in this style. Make it sound like a news article and less like a summary. I want it to sound like something that came out of Gossip Girls or TheShadeRoom not something written by ChatGPT. Remember, you are a teenage girl writing the article like you would celeb drama and tea. That is your audience. So you go girl"
                    }]
                )

                # Extract generated article
                generated_article = response.choices[0].message.content

                # Return the generated article as JSON response
                return jsonify({"article": generated_article})
            else:
                return jsonify({"error": "Failed to download audio file"})
        else:
            return jsonify({"error": "No episodes found or failed to fetch episodes"})
    else:
        return jsonify({"error": "Search failed"})

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(debug=True)
