import http.client
import json
# do not add https to var
from dotenv import load_dotenv
import os
# Load environment variables from .env file
from datetime import datetime, timedelta
import requests

def get_token_from_api():
    conn = http.client.HTTPSConnection(os.getenv("auth0_domain"))
    with open('<credentials_api.json> path') as f:
        data = json.load(f)
    payload = json.dumps(data)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = json.loads(data.decode("utf-8"))
    return response["access_token"]


def get_cached_token(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            token = data['token']
            timestamp = data['timestamp']

            if (datetime.now() - datetime.fromtimestamp(timestamp)) > timedelta(days=1):
                # Token is older than a day, get a new one
                new_token = get_token_from_api()  # Replace with your token retrieval logic
                update_token_file(file_path, new_token)
                return new_token
            return token

    except FileNotFoundError:
        # File not found, get a new token and save it
        new_token = get_token_from_api()
        update_token_file(file_path, new_token)
        return new_token



def update_token_file(file_path, new_token):
    # Use the 'my_token' for your API requests 
    with open(file_path, 'w') as f:
        data = {'token': new_token, 'timestamp': int(datetime.now().timestamp())}
        json.dump(data, f)



# Usage
def put_data_to_db(video):
    load_dotenv()
    token_file = 'token_cache.json' 
    my_token = get_cached_token(token_file)
    headers = { 'Authorization': "Bearer "+my_token ,
                'Content-type': 'application/json'}

    # add https to var
    url = os.getenv("db_archive_domain")+"/file/public"

    video_data = {
        'title': video.name,
        'image_url': video.image_url,
        'description': video.description,
        'link': video.link, 
        'keywords': video.keywords,
        'script':video.script,
        'images': video.images_query,
        'hashtags': video.hashtags,
    }

    response = requests.post(url, headers=headers, json=video_data)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")