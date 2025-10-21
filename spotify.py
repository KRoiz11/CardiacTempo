from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")


# gets token required for all future requests
def get_token(code):
    auth_string = client_id + ":" + client_secret
    auth_bytes =  auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        "code" : code,
        "redirect_uri" : redirect_uri,
        "grant_type" : "authorization_code"
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# function that replaces headers on all future requests
def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


# def get_track_audio_features(token, song_name):
#     track_id = search(token, song_name)
#     url = f"https://api.spotify.com/v1/audio-features/{track_id}"
#     headers = get_auth_header(token)

#     r = requests.get(url, headers=headers)
#     r.raise_for_status
#     items = r.json()["track"]
#     return items["tempo"]


def search(token, song_name):
    headers = get_auth_header(token)
    params = {f"q": {song_name}, "type": "track", "limit": 1}

    r = get("https://api.spotify.com/v1/search", headers=headers, params=params)
    r.raise_for_status()
    items = r.json()["tracks"]["items"]
    if items:
        track_id = items[0]["id"]
        print(track_id)
        return track_id
    
def get_current_user_playlist(token, name):
    headers = get_auth_header(token)
    url = "https://api.spotify.com/v1/me/playlists"

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    items = json_result["items"]
    for playlist in items:
        if playlist["name"] == name:
            return playlist["id"]
        
def get_playlist_items(token, playlist_id, offset):
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    query = {
        "fields" : "items(track(name, id))",
        "limit" : "40",
        "offset" : offset 
        }

    result = get(url, headers=headers, params=query)
    print(result.status_code)
    json_result = result.json()
    items = json_result["items"]
    #print(items)
    track_ids = [track["track"]["id"] for track in items]
    return track_ids

    # track_name = track["name"]
    # track_id = track["id"]
    # return track_name, track_id

def get_playlist_length(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    query = {"fields": "total"}

    result = get(url, headers=headers, params=query)
    json_result = result.json()
    return json_result["total"]