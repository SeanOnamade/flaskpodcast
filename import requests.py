import requests
import time
import hashlib


api_key = "SVJYC3EM7ANXGEUXMZYE"
api_secret = "VF3r5^WT2nZK8Z6FqRsHCA5aCZWc9eMrEFFMJ8V$"
current_time = str(int(time.time()))
encoded_api_key = api_key.encode('utf-8')
encoded_api_secret = api_secret.encode('utf-8')
encoded_current_time = current_time.encode('utf-8')
hash_input = encoded_api_key + encoded_api_secret + encoded_current_time

# Make a sample GET request
search_query = "Everybody's Crazy"
url = f"https://api.podcastindex.org/api/1.0/search/byterm?q={search_query}"

headers = {
    "X-Auth-Date": current_time,  # You may need to replace this with a valid timestamp
    "X-Auth-Key": api_key,
    "User-Agent": "podcaster",  # You may need to replace this with your user agent,
    "Authorization": hashlib.sha1(hash_input).hexdigest()
}

# Print the headers of the response
try:
    response = requests.get(url, headers=headers)
    # Print the response status code
    print("Response Status Code:", response.status_code)

    # Print the response content
    print("Response Content:", response.content)

    # Check if response content is JSON and print it
    try:
        json_response = response.json()
        print("JSON Response:", json_response)
    except ValueError:
        print("Response is not in JSON format")
except Exception as e:
    print("An error occurred:", e)