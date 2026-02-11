from requests import get
import json


def get_recco_track_ids(track_ids):
    
    url = f"https://api.reccobeats.com/v1/track"
    headers = {"Accept": "application/json"}
    query = {"ids": ",".join(track_ids)}

    result = get(url, headers=headers, params=query)
    result.raise_for_status()
    json_result = result.json()
    # print(json_result)
    reccobeats_track_ids = [(track["id"], track["trackTitle"]) for track in json_result["content"]]
    # print()
    # print(reccobeats_track_ids)
    return reccobeats_track_ids

def get_track_features(track_id):
    url = f"https://api.reccobeats.com/v1/track/{track_id}/audio-features"
    headers = {"Accept": "application/json"}


    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()

    return json_result

def get_multiple_track_features(items):
    url = "https://api.reccobeats.com/v1/audio-features"
    headers = {"Accept": "application/json"}
    query = {"ids": items}

    result = get(url, headers=headers, params=query)
    result.raise_for_status()
    json_result = result.json()

    return json_result

    